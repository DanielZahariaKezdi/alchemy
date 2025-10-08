from fastapi import APIRouter

router = APIRouter(prefix = '/authors', tags = ['authors'])

@router.get('/')

def get_authors():
    print('Welcome to the authors page')