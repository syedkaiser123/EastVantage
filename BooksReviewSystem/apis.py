
from fastapi import FastAPI, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from api_models.models import Book, BookSchema, Review, ReviewSchema
from databases.database_config import SessionLocal
import logging
from tasks import send_confirmation_email

def create_book(db: Session, book_data: Book):
    '''
    This method is used to add book details like:

    title: str
    author: str
    publication_year: str
    '''
    db_book = Book(**book_data.dict())
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book

def create_review(db: Session, book_id: int, review_data: Review, background_tasks: BackgroundTasks):
    '''
    This method is used to add a review for a given book id.

    text: str
    rating: int
    '''
    db_review = Review(**review_data.dict(), book_id=book_id)
    db.add(db_review)
    db.commit()
    db.refresh(db_review)
    #creating a background task for sending a confirmation email to the reviewer.
    background_tasks.add_task(send_confirmation_email, "", db_review.id)
    return db_review

def get_books(db: Session, author: str = None, publication_year: int = None):
    '''
    This method is used to get all the books for the given filters:

    author: str
    publication_year: int
    '''
    query = db.query(Book)
    if author:
        query = query.filter(Book.author == author)
    if publication_year:
        query = query.filter(Book.publication_year == publication_year)
    return query.all()

def get_reviews(db: Session, book_id: int):
    '''
    This method is used to retrieve all the reviews of a given book id
    '''
    return db.query(Review).filter(Review.book_id == book_id).all()
