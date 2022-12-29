from fastapi import FastAPI
from pydantic import BaseModel, Field
from uuid import UUID
from typing import Optional

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


BOOKS = []


@app.get("/")
async def read_all_books(books_to_return: Optional[int] = None):
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

@app.post("/")
async def create_book(book: Book):
    # book of type Book (class we made)
    BOOKS.append(book)
    return book


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



