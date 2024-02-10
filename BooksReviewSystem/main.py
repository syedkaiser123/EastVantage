
from fastapi import FastAPI, Depends, HTTPException, BackgroundTasks
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from databases.database_config import SessionLocal, engine, Base
from api_models.models import Book
from api_models.models import Review, BookSchema, ReviewSchema
import apis
import tasks

app = FastAPI()

# Create tables
Base.metadata.create_all(bind=engine)

# Dependency to get database session.
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Using Dependency injection to handle database sessions for each request as Depends(get_db).
@app.post("/books/", response_model=BookSchema)
def add_book(book_data: BookSchema, db: Session = Depends(get_db)):
    '''
    This endpoint will add book details such as:

    title: str
    author: str
    publicaton_year: int
    '''
    try:
        created_book = apis.create_book(db=db, book_data=book_data)
        return {
            'title': f'{created_book.title}',
            'author': f'{created_book.author}',
            'publication_year': f'{created_book.publication_year}'
        }
    except Exception as e:
        print(f"Error creating book: {e}")
        # Rollback the transaction to maintain consistency
        db.rollback()
        return {"success": False, "error": str(e)}

@app.post("/books/{book_id}/reviews/", response_model=ReviewSchema)
def submit_review(book_id: int, review_data: ReviewSchema, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    '''
    This endpoint will submit reviews for a particular book.
    '''
    try:
        # Fetch the book corresponding to the provided book_id
        book = db.query(Book).filter(Book.book_id == book_id).first()
        if book is None:
            raise HTTPException(status_code=404, detail="Book not found")
        review_data = apis.create_review(db=db, review_data=review_data, book_id=book_id, background_tasks=background_tasks)
        return {
                "title": book.title,
                "text": f'{review_data.text}',
                "rating": f'{review_data.rating}',
        }
    except Exception as e:
        return {"Error": str(e)}

@app.get("/books/", response_model=list[BookSchema])
def get_books(author: str = None, publication_year: int = None, db: Session = Depends(get_db)):
    '''
    This endpoint will retrieve all books for the given filters:

    author: str
    publication_year: int
    '''
    try:
        return apis.get_books(db=db, author=author, publication_year=publication_year)
    except Exception as e:
        return {"Error": str(e)}

@app.get("/books/{book_id}/reviews/", response_model=list[ReviewSchema])
def get_reviews(book_id: int, db: Session = Depends(get_db)):
    '''
    This endpoint will retrieve all reviews for a given book.
    '''
    try:
        return apis.get_reviews(db=db, book_id=book_id)
    except Exception as e:
        return {"Error": str(e)}

from fastapi import HTTPException

@app.delete("/books/{book_id}/")
def delete_book(book_id: int, db: Session = Depends(get_db)):
    '''
    This endpoint is used to delete a particular book details.
    '''
    try:
        # Fetch the book corresponding to the provided book_id
        book = db.query(Book).filter(Book.book_id == book_id).first()
        
        # Check if the book exists
        if book is None:
            raise HTTPException(status_code=404, detail="Book not found")
        
        # Delete the book
        db.delete(book)
        db.commit()
        
        return {"message": "Book deleted successfully"}
    
    except Exception as e:
        return {"Error": str(e)}

@app.put("/books/{book_id}/")
def update_book(book_id: int, book_update: BookSchema, db: Session = Depends(get_db)):
    '''
    This endpoint will update a specific book details based on the given book_id.
    '''
    try:
        # Fetch the book corresponding to the provided book_id
        book = db.query(Book).filter(Book.book_id == book_id).first()
        
        # Check if the book exists
        if book is None:
            raise HTTPException(status_code=404, detail="Book not found")
        
        # Update the book details
        book.title = book_update.title
        book.author = book_update.author
        book.publication_year = book_update.publication_year

        # Commit the changes to the database
        db.commit()

        return {"message": "Book details updated successfully"}
    
    except Exception as e:
        return {"Error": str(e)}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
