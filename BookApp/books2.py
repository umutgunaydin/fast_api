from typing import Optional
from fastapi import Body, FastAPI, Path, Query, HTTPException
from pydantic import BaseModel, Field
from starlette import status

app = FastAPI()

class Book:
    id: int
    title: str
    author: str
    description: str
    rating: int
    published_date: int

    def __init__(self, id: int, title: str, author: str, description: str, rating: int, published_date: int):
        self.id = id
        self.title = title
        self.author = author
        self.description = description
        self.rating = rating
        self.published_date = published_date
class BookRequest(BaseModel):
    id: Optional[int] = Field(default=None, description="The id is optional")  
    title: str = Field(min_length=3, max_length=20)
    author: str = Field(min_length=3, max_length=20)
    description: str = Field(min_length=3, max_length=200)
    rating: int = Field(gt=0, lt=6)
    published_date: int = Field(default=2024, description="The published date is optional")

    class Config:
        json_schema_extra = {
            "example": {
                "title": "Title One",
                "author": "Author One",
                "description": "Description One",
                "rating": 5
            }
        }


BOOKS=[
    Book(1, 'Title One', 'Author One', 'Description One', 5, 2024),
    Book(2, 'Title Two', 'Author Two', 'Description Two', 4, 2023),
    Book(3, 'Title Three', 'Author Three', 'Description Three', 3, 2022),
    Book(4, 'Title Four', 'Author Four', 'Description Four', 2, 2021),
    Book(5, 'Title Five', 'Author Five', 'Description Five', 1, 2020),
    Book(6, 'Title Five', 'Author Five', 'Description Five', 1, 2020)
]

@app.get("/books", status_code=status.HTTP_200_OK)
async def get_all_books():
    return BOOKS

@app.get("/books/{book_id}", status_code=status.HTTP_200_OK)
async def get_book_by_id(book_id: int = Path(gt=0)):
    for book in BOOKS:
        if book.id == book_id:
            return book
    raise HTTPException(status_code=404, detail="Book not found")

@app.get("/books/", status_code=status.HTTP_200_OK)
async def get_books_by_rating(rating: int = Query(ge=1, le=5)):
    return [book for book in BOOKS if book.rating == rating]

@app.get("/books/{published_date}/published_date/", status_code=status.HTTP_200_OK)
async def get_books_by_published_date(published_date: int):
    return [book for book in BOOKS if book.published_date == published_date]

@app.post("/books/create_book/", status_code=status.HTTP_201_CREATED)
async def create_book(book_request : BookRequest):
    new_book = Book(**book_request.model_dump())
    BOOKS.append(assign_book_id(new_book))
    return new_book

@app.put("/books/update_book", status_code=status.HTTP_200_OK)
async def update_book(book_request: BookRequest):
    update_book = False
    for book in BOOKS:
        if book.id == book_request.id:
            BOOKS.remove(book)
            book = Book(**book_request.model_dump())
            BOOKS.append(book)
            update_book = True
    if not update_book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book

@app.delete("/books/delete_book/{book_id}" , status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(book_id: int = Path(gt=0)):
    book = find_book_by_id(book_id)
    if book:
        BOOKS.remove(book)
        is_deleted = True
        return {"message": "Book deleted successfully"}
    raise HTTPException(status_code=404, detail="Book not found")    


def assign_book_id(book: Book):
    book.id = 1 if len(BOOKS) == 0 else BOOKS[-1].id + 1
    return book

def find_book_by_id(book_id: int):
    for book in BOOKS:
        if book.id == book_id:
            return book
    return None