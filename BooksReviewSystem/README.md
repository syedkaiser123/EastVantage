# Book Review System

The Book Review System is a RESTful API built using FastAPI for managing book reviews. It allows users to add new books, submit reviews for books, retrieve books with filtering options, and retrieve reviews for specific books. The application integrates with a SQLite database for data persistence.

## Features

- Add a new book with title, author, and publication year
- Submit a review for a book with text review and rating
- Retrieve all books with optional filtering by author or publication year
- Retrieve all reviews for a specific book
- Data validation using Pydantic models
- Error handling for invalid requests
- Integration with SQLite database for data persistence
- CRUD operations for books and reviews
- Background task for sending confirmation emails after review submission
- Testing of API endpoints using FastAPI's test client

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/syedkaiser123/EastVantage.git
2. Navigate to the project repository:
    ```bash
    cd EastVantage/BooksReviewSystem/
3. Install the dependencies:
    ```bash
    pip install -r requirements.txt
4. Run the application:
    ```bash
    uvicorn main:app --reload

## Usage
- Use an API client like Postman or cURL to interact with the API endpoints.
## Endpoint URLs
- `POST: http://127.0.0.1:8000/books/`
- `POST: http://127.0.0.1:8000/books/{book_id}/reviews/`
- `GET: http://127.0.0.1:8000/books/{book_id}/reviews/`
- `DELETE: http://127.0.0.1:8000/books/{book_id}`
- `PUT: http://127.0.0.1:8000/books/{book_id}`

### `Note`: You can also refer or import the postman collection I have provided in the repository above.

## Testing
### `Note`: The test cases are not working yet as there is some module level issue. However, I have completed test cases for all the endpoints in the above application.
- Run the test cases using pytest:
    ```
    pytest
    ```

