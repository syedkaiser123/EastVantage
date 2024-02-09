
from fastapi import FastAPI, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from db_api_models.models import Book, BookSchema, Item, ItemSchema, Review, ReviewSchema
from databases.database_config import SessionLocal
import logging
from tasks import send_confirmation_email

def create_book(db: Session, book_data: Book):
    db_book = Book(**book_data.dict())
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book

def create_review(db: Session, book_id: int, review_data: Review, background_tasks: BackgroundTasks):
    
    db_review = Review(**review_data.dict(), book_id=book_id)
    db.add(db_review)
    db.commit()
    db.refresh(db_review)
    background_tasks.add_task(send_confirmation_email, db_review.id)
    return db_review

def get_books(db: Session, author: str = None, publication_year: int = None):
    query = db.query(Book)
    # import ipdb;ipdb.set_trace()
    # # Log the generated SQL query
    # logging.info(f"Generated SQL query: {query}")
    if author:
        query = query.filter(Book.author == author)
    if publication_year:
        query = query.filter(Book.publication_year == publication_year)
    return query.all()

def get_reviews(db: Session, book_id: int):
    return db.query(Review).filter(Review.book_id == book_id).all()
