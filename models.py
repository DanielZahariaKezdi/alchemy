from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, Integer, String
from database import Base

class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(32), nullable=False)
    password: Mapped[str] = mapped_column(String(32), nullable=False)

class Author(Base):
    __tablename__ = 'authors'

    id: Mapped[int] = mapped_column(primary_key=True)
    author_name: Mapped[str] = mapped_column(String(32), nullable=False)

    # relations
    books: Mapped[list['Book']] = relationship('Book', back_populates = 'author')

class Book(Base):
    __tablename__ = 'books'

    id: Mapped[int] = mapped_column(primary_key=True)
    book_title: Mapped[str] = mapped_column(String(32), nullable=False)
    author_id: Mapped[int] = mapped_column(ForeignKey("authors.id"), nullable=False)

    # relations
    author: Mapped["Author"] = relationship(back_populates="books")

class Loan(Base):
    __tablename__ = "loans"

    pass