from fastapi import APIRouter

router = APIRouter(prefix = '/stats', tags = ['stats'])

@router.get('/')

def get_stats():
    print('Welcome to the stats page')