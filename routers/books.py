from fastapi import APIRouter

router = APIRouter(prefix = '/books', tags = ['books'])

@router.get('/')

def get_animals():
    print('Welcome to the animal page')