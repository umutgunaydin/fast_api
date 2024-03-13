from fastapi import Body, FastAPI

app = FastAPI()

class Book:
    id: int
    title: str
    author: str
    description: str
    rating: int

    def __init__(self, id: int, title: str, author: str, description: str, rating: int):
        self.id = id
        self.title = title
        self.author = author
        self.description = description
        self.rating = rating


BOOKS=[
    Book(1, 'Title One', 'Author One', 'Description One', 5),
    Book(2, 'Title Two', 'Author Two', 'Description Two', 4),
    Book(3, 'Title Three', 'Author Three', 'Description Three', 3),
    Book(4, 'Title Four', 'Author Four', 'Description Four', 2),
    Book(5, 'Title Five', 'Author Five', 'Description Five', 1)
]

@app.get("/books")
async def get_all_books():
    return BOOKS

@app.post("/books/create_book/")
async def create_book(new_book = Body()):
    BOOKS.append(new_book)
    return new_book