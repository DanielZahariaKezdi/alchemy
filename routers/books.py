from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from db import sessionlocal
from schemas import BookCreate, BookResponse
from models import Book, Author

router = APIRouter(prefix='/books', tags=['books'])

def get_db():
    db = sessionlocal()
    try:
        yield db
    finally:
        db.close()

@router.get('/', response_model=list[BookResponse])
def get_books(db: Session = Depends(get_db)):
    books = db.query(Book).all()
    return books

@router.get('/{book_id}', response_model=BookResponse)
def get_book(book_id: int, db: Session = Depends(get_db)):
    book = db.query(Book).filter(Book.id == book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book

@router.post('/add', response_model=BookResponse)
def create_book(book: BookCreate, db: Session = Depends(get_db)):



    author = db.query(Author).filter(Author.id == book.author_id).first()
    if not author:
        raise HTTPException(status_code=404, detail="Author not found")
    
    new_book = Book(book_title=book.book_title, author_id=book.author_id)
    db.add(new_book)
    db.commit()
    db.refresh(new_book)
    return new_book

@router.put('/{book_id}', response_model=BookResponse)
def update_book(book_id: int, book: BookCreate, db: Session = Depends(get_db)):
    db_book = db.query(Book).filter(Book.id == book_id).first()
    if not db_book:
        raise HTTPException(status_code=404, detail="Book not found")
    

    author = db.query(Author).filter(Author.id == book.author_id).first()
    if not author:
        raise HTTPException(status_code=404, detail="Author not found")
    
    db_book.book_title = book.book_title
    db_book.author_id = book.author_id
    db.commit()
    db.refresh(db_book)
    return db_book

@router.delete('/{book_id}')
def delete_book(book_id: int, db: Session = Depends(get_db)):
    book = db.query(Book).filter(Book.id == book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    
    db.delete(book)
    db.commit()
    return {"message": f"Book '{book.book_title}' deleted successfully"}