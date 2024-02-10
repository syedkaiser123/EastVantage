from fastapi.testclient import TestClient
from BooksReviewSystem.main import app
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from databases.database_config import Base, engine
from models.models import Book, Review

# Create an SQLAlchemy session to interact with the database
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Function to setup and tear down the test database
def setup_test_db():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

# Function to override dependency for testing
def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

# Initialize the test client
client = TestClient(app)

def test_add_book():
    book_data = {"title": "Test Book", "author": "Test Author", "publication_year": 2022}
    response = client.post("/books/", json=book_data)
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Test Book"
    assert data["author"] == "Test Author"
    assert data["publication_year"] == 2022

def test_add_book_invalid_data():
    book_data = {"title": "Test Book", "publication_year": "2022"}  # Missing "author" field
    response = client.post("/books/", json=book_data)
    assert response.status_code == 422  # 422 Unprocessable Entity

def test_submit_review():
    book_data = {"title": "Test Book", "author": "Test Author", "publication_year": 2022}
    response = client.post("/books/", json=book_data)
    assert response.status_code == 200
    book_id = response.json()["id"]
    review_data = {"text_review": "Great book!", "rating": 5}
    response = client.post(f"/books/{book_id}/reviews/", json=review_data)
    assert response.status_code == 200
    data = response.json()
    assert data["text_review"] == "Great book!"
    assert data["rating"] == 5

def test_get_books():
    response = client.get("/books/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)

def test_get_reviews():
    book_data = {"title": "Test Book", "author": "Test Author", "publication_year": 2022}
    response = client.post("/books/", json=book_data)
    assert response.status_code == 200
    book_id = response.json()["id"]
    review_data = {"text_review": "Great book!", "rating": 5}
    response = client.post(f"/books/{book_id}/reviews/", json=review_data)
    assert response.status_code == 200
    response = client.get(f"/books/{book_id}/reviews/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)

if __name__ == "__main__":
    setup_test_db()
