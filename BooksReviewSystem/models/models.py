
from pydantic import BaseModel

class Item(BaseModel):
    name: str
    description: str = None
    price: float
    tax: float = None

class Book(BaseModel):
    title: str
    author: str
    publication_year: int

class Review(BaseModel):
    text: str
    rating: int

