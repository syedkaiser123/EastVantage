
from fastapi import FastAPI, Depends, HTTPException, BackgroundTasks
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from databases.database_config import SessionLocal, engine, Base
from models.models import Book as book_model
from models.models import Review as review_model
import apis
import tasks

app = FastAPI()

# Create tables
Base.metadata.create_all(bind=engine)

# Dependency to get database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/books/", response_model=book_model)
def add_book(book_data: book_model, db: Session = Depends(get_db)):
    try:
        return apis.create_book(db=db, book_data=book_data)
    except Exception as e:
        return {"Error": str(e)}

@app.post("/books/{book_id}/reviews/", response_model=review_model)
def submit_review(book_id: int, review_data: review_model, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    try:
        return apis.create_review(db=db, review_data=review_data, book_id=book_id)
    except Exception as e:
        return {"Error": str(e)}

@app.get("/books/", response_model=list[book_model])
def get_books(author: str = None, publication_year: int = None, db: Session = Depends(get_db)):
    try:
        return apis.get_books(db=db, author=author, publication_year=publication_year)
    except Exception as e:
        return {"Error": str(e)}

@app.get("/books/{book_id}/reviews/", response_model=list[review_model])
def get_reviews(book_id: int, db: Session = Depends(get_db)):
    try:
        return apis.get_reviews(db=db, book_id=book_id)
    except Exception as e:
        return {"Error": str(e)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
