from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from db import sessionlocal
from models import Loan, Book, Author, User

router = APIRouter(prefix='/stats', tags=['stats'])

def get_db():
    db = sessionlocal()
    try:
        yield db
    finally:
        db.close()

@router.get('/')
def get_stats(db: Session = Depends(get_db)):
    loans = db.query(Loan).all()
    
    books_on_loan = []
    for loan in loans:
        book = db.query(Book).filter(Book.id == loan.book_id).first()
        author = db.query(Author).filter(Author.id == book.author_id).first()
        user = db.query(User).filter(User.id == loan.user_id).first()
        
        books_on_loan.append({
            'loan_id': loan.id,
            'book_title': book.book_title,
            'author_name': author.author_name,
            'borrowed_by': user.name
        })
    
    return {
        "total_books_loan": len(books_on_loan),
        "books": books_on_loan
    }