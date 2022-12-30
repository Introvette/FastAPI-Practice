from fastapi import FastAPI, HTTPException, Request, status, Form, Header
from pydantic import BaseModel, Field
from uuid import UUID
from typing import Optional
from starlette.responses import JSONResponse


class NegativeNumberException(Exception):
    def __init__(self, books_to_return):
        self.books_to_return = books_to_return


app = FastAPI()


class Book(BaseModel):
    id: UUID
    title: str = Field(min_length=1)
    # adding Field to a property value makes it so data is validated correctly
    # and can't be an empty string when running it on swagger, kind of like Django models
    author: str = Field(min_length=1, max_length=100)
    description: Optional[str] = Field(title="Description of the book", max_length=100, min_length=1)
    rating: int = Field(gt=-1, lt=101)
    # this field for rating means the rating needs to be greater than (gt) -1
    # and less than (lt) 101
    # rating should never be over 100

    class Config:
        schema_extra = {
            # this adds an example response body to our swagger UI
            'example': {
                'id': '1833c191-7f5e-4866-83e2-489b41083e56',
                'title': 'Computer Science Pro',
                'author': 'CodingwithRoby',
                'description': 'an awesome book',
                'rating': 75


            }
        }


class BookNoRating(BaseModel):
    id: UUID
    title: str = Field(min_length = 1)
    author: str
    description: Optional[str] = Field(None, title="description of the Book", min_length=1, max_length=100)


BOOKS = []


@app.exception_handler(NegativeNumberException)
async def negative_number_exception_handler(request: Request,
                                            exception: NegativeNumberException):
    return JSONResponse(
        status_code=418,
        content={"message": f"Hey, why do you want {exception.books_to_return}"
                f"books? You need to read more!"}
    )


@app.post('/books/login')
async def books_login(username: str = Form(...), password: str = Form(...)):
    # ^^ no longer need the "..." in new FastAPI version
    return {"username": username, "password": password}

@app.get("/header")
async def read_header(random_header: Optional[str] = Header(None)):
    return {"random_header": random_header}

@app.get("/")
async def read_all_books(books_to_return: Optional[int] = None):
    if books_to_return and books_to_return < 0:
        raise NegativeNumberException(books_to_return=books_to_return)
    if len(BOOKS) < 1:
        # if there are no books in BOOKS empty list then we're going to use
        # the books we made down below
        create_books_no_api()
    if books_to_return and len(BOOKS) >= books_to_return > 0:
        i = 1
        new_books = []
        while i <= books_to_return:
            new_books.append(BOOKS[i-1])
            i += 1
        return new_books
    return BOOKS


@app.get("/book/{book_id}")
async def read_book(book_id: UUID):
    for x in BOOKS:
        if x.id == book_id:
            return x
    raise raise_item_cannot_be_found_exception()


@app.get("/book/rating/{book_id}", response_model=BookNoRating)
async def read_book_no_rating(book_id: UUID):
    for x in BOOKS:
        if x.id == book_id:
            return x
    raise raise_item_cannot_be_found_exception()
# this eliminates the rating when sending a request to get details of a book without the rating


@app.post("/", status_code=status.HTTP_201_CREATED)
async def create_book(book: Book):
    # book of type Book (class we made)
    BOOKS.append(book)
    return book


@app.put("/{book_id}")
async def update_book(book_id: UUID, book: Book):
    counter = 0
    for x in BOOKS:
        counter += 1
        if x.id == book_id:
            BOOKS[counter - 1] = book
            return BOOKS[counter - 1]
    raise raise_item_cannot_be_found_exception()


@app.delete("/{book_id}")
async def delete_book(book_id: UUID):
    # book type : UUID
    counter = 0
    for x in BOOKS:
        counter += 1
        if x.id == book_id:
            del BOOKS[counter - 1]
            return f'ID:{book_id} deleted'
        # raise exception for when book_id does not exist
    raise raise_item_cannot_be_found_exception()


def create_books_no_api():
    book_1 = Book(id="b833c191-7f5e-4866-83e2-489b41083e56",
                  title= "Title One",
                  author= "Author One",
                  description= "Description 1",
                  rating=60)
    book_2 = Book(id="330bedd3-90cb-4457-898b-53bed7ea0d46",
                  title= "Title Two",
                  author= "Author Two",
                  description= "Description 2",
                  rating=90)
    book_3 = Book(id="e3560404-26e3-4faf-a929-c519728876bc",
                  title= "Title Three",
                  author= "Author Three",
                  description= "Description 3",
                  rating=30)
    book_4 = Book(id="cd421851-fbc5-4176-bd09-1c9a94327e1f",
                  title= "Title Four",
                  author= "Author Four",
                  description= "Description 4",
                  rating=75)
    BOOKS.append(book_1)
    BOOKS.append(book_2)
    BOOKS.append(book_3)
    BOOKS.append(book_4)


def raise_item_cannot_be_found_exception():
    return HTTPException(status_code=404, detail="Book not found", headers={"X-Header_Error": "Nothing to be seen at this UUID"})
# this is a separate function to be called in the delete function or any function that may query for an UUID that may not exist.