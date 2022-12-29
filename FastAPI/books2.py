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
    author: str
    description: Optional[str] = Field(title="Description of the book", max_length=100, min_length=1, )
    rating: int


BOOKS = []

@app.get("/")
async def read_all_books():
    return BOOKS

@app.post("/")
async def create_book(book: Book):
    # book of type Book (class we made)
    BOOKS.append(book)
    return book