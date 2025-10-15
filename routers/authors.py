from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from db import sessionlocal
from schemas import AuthorCreate, AuthorResponse
from models import Author

router = APIRouter(prefix='/authors', tags=['authors'])

def get_db():
    db = sessionlocal()
    try:
        yield db
    finally:
        db.close()

@router.get('/', response_model=list[AuthorResponse])
def get_authors(db: Session = Depends(get_db)):
    authors = db.query(Author).all()
    return authors

@router.get('/{author_id}', response_model=AuthorResponse)
def get_author(author_id: int, db: Session = Depends(get_db)):
    author = db.query(Author).filter(Author.id == author_id).first()
    if not author:
        raise HTTPException(status_code=404, detail="Author not found")
    return author

@router.post('/add', response_model=AuthorResponse)
def create_author(author: AuthorCreate, db: Session = Depends(get_db)):
    new_author = Author(author_name=author.author_name)
    db.add(new_author)
    db.commit()
    db.refresh(new_author)
    return new_author

@router.put('/{author_id}', response_model=AuthorResponse)
def update_author(author_id: int, author: AuthorCreate, db: Session = Depends(get_db)):
    db_author = db.query(Author).filter(Author.id == author_id).first()
    if not db_author:
        raise HTTPException(status_code=404, detail="Author not found")
    
    db_author.author_name = author.author_name
    db.commit()
    db.refresh(db_author)
    return db_author

@router.delete('/{author_id}')
def delete_author(author_id: int, db: Session = Depends(get_db)):
    author = db.query(Author).filter(Author.id == author_id).first()
    if not author:
        raise HTTPException(status_code=404, detail="Author not found")
    
    if author.books:
        raise HTTPException(
            status_code=400, 
            detail=f"Cannot delete author. Author has {len(author.books)}."
        )
    
    db.delete(author)
    db.commit()
    return {'message': f'Author {author.author_name} deleted'}