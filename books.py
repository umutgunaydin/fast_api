from fastapi import Body, FastAPI

app = FastAPI()

BOOKS = [
    {'title': 'Title One', 'author': 'Author One', 'category': 'science'},
    {'title': 'Title Two', 'author': 'Author Two', 'category': 'science'},
    {'title': 'Title Three', 'author': 'Author Three', 'category': 'history'},
    {'title': 'Title Four', 'author': 'Author Four', 'category': 'math'},
    {'title': 'Title Five', 'author': 'Author Five', 'category': 'math'},
    {'title': 'Title Six', 'author': 'Author Two', 'category': 'math'}
]

@app.get("/books")
async def get_all_books():
    return BOOKS

@app.get("/books/{book_title}")
async def get_book_by_title(book_title: str):
    for book in BOOKS:
        if book['title'] == book_title:
            return book
        
@app.get("/books/{author}/author")
async def get_books_by_author(author: str):
    books_to_return = []
    for book in BOOKS:
        if book['author'].casefold() == author.casefold():
            books_to_return.append(book)
    return books_to_return
        
@app.get("/books/")
async def get_books_by_category_by_query(author: str, category: str):
    books_to_return = []
    for book in BOOKS:
        if book['category'] == category and book['author'] == author:
            books_to_return.append(book)
    return books_to_return

@app.post("/books/create_book/")
async def create_book(new_book: dict = Body()):
    BOOKS.append(new_book)
    return new_book

@app.put("/books/update_book}")
async def update_book(updated_book: dict = Body()):
    for book in BOOKS:
        if book['title'].casefold() == updated_book['title'].casefold():
            book.update(updated_book)
            return book
        
@app.delete("/books/delete_book/{book_title}")
async def delete_book(book_title: str):
    for book in BOOKS:
        if book['title'].casefold() == book_title.casefold():
            BOOKS.remove(book)
            return {"message": "Book deleted successfully!"}
    return {"message": "Book not found!"}