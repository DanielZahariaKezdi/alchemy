import uvicorn
from fastapi import FastAPI
from database import engine
from routers import users_router, book_router, authors_router, stats_router

app = FastAPI()

@app.get('/')

def get_root():
    print('Welcome to the Alchemy project')

@app.get('/test-db')

def test_db():
    try:
        with engine.connect() as konekt:
            print("Connection successfull: ", konekt)
    except Exception as exception:
        print("Unable to connect: ", exception)

app.include_router(users_router)
app.include_router(book_router)
app.include_router(authors_router)
app.include_router(stats_router)

if __name__ == '__main__':

    uvicorn.run('main:app', host = '127.0.0.1', port = 8000, reload = True)



