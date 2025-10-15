from pydantic import BaseModel

class UserCreate(BaseModel):
    name: str
    password: str

class UserResponse(BaseModel):
    id: int
    name: str
    
    class Config:
        from_attributes = True

class AuthorCreate(BaseModel):
    author_name: str

class AuthorResponse(BaseModel):
    id: int
    author_name: str
    
    class Config:
        from_attributes = True

class BookCreate(BaseModel):
    book_title: str
    author_id: int

class BookResponse(BaseModel):
    id: int
    book_title: str
    author_id: int
    
    class Config:
        from_attributes = True

class BookWithAuthor(BaseModel):
    id: int
    book_title: str
    author: AuthorResponse
    
    class Config:
        from_attributes = True

class LoanCreate(BaseModel):
    book_id: int
    user_id: int

class LoanResponse(BaseModel):
    id: int
    book_id: int
    user_id: int
    
    class Config:
        from_attributes = True