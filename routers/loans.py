from fastapi import APIRouter

router = APIRouter(prefix = '/loans', tags = ['loans'])

@router.get('/')

def get_loans():
    print('Welcome to the loan page')