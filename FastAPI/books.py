from fastapi import FastAPI
from enum import Enum
from typing import Optional

app = FastAPI()

BOOKS = {
    'book_1': {'title': 'Title One', 'author': 'Author One'},
    'book_2': {'title': 'Title Two', 'author': 'Author Two'},
    'book_3': {'title': 'Title Three', 'author': 'Author Three'},
    'book_4': {'title': 'Title Four', 'author': 'Author Four'},
    'book_5': {'title': 'Title Five', 'author': 'Author Five'},
}

# class DirectionName(str, Enum):
#     north = "North"
#     south = "South"
#     east = "East"
#     west = "West"


@app.get("/")
async def read_all_books(skip_book: Optional[str] = None):
    # When you make it equal to None, FastAPI knows automatically that this is going to be an optional call
    if skip_book:
        new_books = BOOKS.copy()
        del new_books[skip_book]
        return new_books
    return BOOKS

@app.get("/{book_name}")
async def read_book(book_name: str):
    #typehingting!! ^^^^
    return BOOKS[book_name]
# returning a book name from the BOOKS dictionary

@app.get("books/mybook")
async def read_favorite_book():
    return {"book_title": "My favorite book"}

@app.get("/books/{book_id}")
async def read_book(book_id: int):
    # can add int in the parameters to make sure  it has to be an integer
    # parameter is book_title which is what we want in our response
    return {"book_title": book_id}

@app.post("/")
async def create_book(book_title, book_author):
    current_book_id = 0
    if len(BOOKS) > 0:
        # find length if greater than 0 return list of books
        for book in BOOKS:
            # loop through each book to find out what number
            # is at the end of books_1 or books_2 so we can add one to the
            # largest number within the books
            x = int(book.split('_')[-1])
            # to find last number or character
            if x > current_book_id:
                current_book_id = x
                # want to make sure current book id is equal to x
    BOOKS[f'book_{current_book_id + 1}'] = {'title': book_title, 'author': book_author}
    # create new value/id to create a new book with a book title and author
    return BOOKS[f'book_{current_book_id + 1}']

@app.put("/{book_name}")
async def update_book(book_name: str, book_title: str, book_author: str):
    # book title and author in the typehint is a query parameter and book_name is the path parameter
    book_information = {'title': book_title, 'author': book_author}
    # new dictionary will be created
    BOOKS[book_name] = book_information
    # books at that book name will be equal new book information which is the dict of title and author
    return book_information
    # return new information user requested





# @app.get("/directions/{direction_name}")
# async def get_direction(direction_name: DirectionName):
#     if direction_name == DirectionName.north:
#         return {"Direction": direction_name, "sub": "Up"}
#     if direction_name == DirectionName.south:
#         return {"Direction": direction_name, "sub": "Down"}
#     if direction_name == DirectionName.west:
#         return {"Direction": direction_name, "sub": "Left"}
#     return {"Direction": direction_name, "sub": "Right"}

