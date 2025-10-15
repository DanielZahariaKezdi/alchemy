from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from db import sessionlocal
from schemas import LoanCreate, LoanResponse
from models import Loan, Book, User

router = APIRouter(prefix='/loans', tags=['loans'])

def get_db():
    db = sessionlocal()
    try:
        yield db
    finally:
        db.close()

@router.get('/', response_model=list[LoanResponse])
def get_loans(db: Session = Depends(get_db)):
    loans = db.query(Loan).all()
    return loans

@router.get('/{loan_id}', response_model=LoanResponse)
def get_loan(loan_id: int, db: Session = Depends(get_db)):
    loan = db.query(Loan).filter(Loan.id == loan_id).first()
    if not loan:
        raise HTTPException(status_code=404, detail="Loan not found")
    return loan

@router.post('/add', response_model=LoanResponse)
def create_loan(loan: LoanCreate, db: Session = Depends(get_db)):

    book = db.query(Book).filter(Book.id == loan.book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    

    user = db.query(User).filter(User.id == loan.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    

    existing_loan = db.query(Loan).filter(Loan.book_id == loan.book_id).first()
    if existing_loan:
        raise HTTPException(status_code=400, detail="Book is already on loan")
    
    new_loan = Loan(book_id=loan.book_id, user_id=loan.user_id)
    db.add(new_loan)
    db.commit()
    db.refresh(new_loan)
    return new_loan

@router.put('/{loan_id}', response_model=LoanResponse)
def update_loan(loan_id: int, loan: LoanCreate, db: Session = Depends(get_db)):
    db_loan = db.query(Loan).filter(Loan.id == loan_id).first()
    if not db_loan:
        raise HTTPException(status_code=404, detail="Loan not found")
    

    book = db.query(Book).filter(Book.id == loan.book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    

    user = db.query(User).filter(User.id == loan.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    db_loan.book_id = loan.book_id
    db_loan.user_id = loan.user_id
    db.commit()
    db.refresh(db_loan)
    return db_loan

@router.delete('/{loan_id}')
def delete_loan(loan_id: int, db: Session = Depends(get_db)):
    loan = db.query(Loan).filter(Loan.id == loan_id).first()
    if not loan:
        raise HTTPException(status_code=404, detail="not found")
    
    db.delete(loan)
    db.commit()
    return {"message": f"Loan {loan_id} deleted"}