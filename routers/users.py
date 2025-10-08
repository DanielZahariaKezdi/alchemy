from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from database import sessionlocal
from schemas import UserCreate, UserResponse
from models import User

router = APIRouter(prefix = '/users', tags = ['users'])

def get_db():
    with sessionlocal() as db:
        users = db.query(User).all()
        return users

@router.get('/', response_model = list[UserResponse])

def get_message():
    return {'message': 'this is the user get'}

def get_users(db: Session = Depends(get_db)):
    
    users = db.query(User).all()
    return users

@router.post('/add', response_model = UserResponse)

def post_message():
    return {'message': 'this is the user post page'}

def post_users(user: UserCreate, db: Session = Depends(get_db)):

    new_user = User(name = user.name, password = user.password)

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user
