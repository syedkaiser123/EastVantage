
from pydantic import BaseModel
from sqlalchemy import Column, Integer, String, Float
from databases.database_config import Base
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship




class ItemSchema(BaseModel):
    name: str
    description: str = None
    price: float
    tax: float = None

    class Config:
        orm_mode = True

class Item(Base):
    __tablename__ = 'items'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    description = Column(String)
    price = Column(Float)
    tax = Column(Float)

class Book(Base):
    __tablename__ = 'books'

    book_id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    author = Column(String)
    publication_year = Column(Integer)

    reviews = relationship("Review", back_populates="books")

class BookSchema(BaseModel):
    title: str
    author: str
    publication_year: int

    class Config:
        orm_mode = True

class Review(Base):
    __tablename__ = 'reviews'

    id = Column(Integer, primary_key=True, index=True)
    text = Column(String)
    rating = Column(Integer)

    book = relationship("Book", back_populates="reviews")

class ReviewSchema(BaseModel):
    text: str
    rating: int

    class Config:
        orm_mode = True
