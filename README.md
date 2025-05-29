# Book API

A RESTful API for managing books, authors, publishers, and reviews built with Django and Django REST Framework.

## Project Overview

This API provides endpoints for managing a book catalog system with the following features:

- CRUD operations for books, authors, publishers, and reviews
- Search, filter, and ordering capabilities
- Token-based authentication
- Interactive API documentation with Swagger and ReDoc
- Permissions: read-only for anonymous users, full access for authenticated users

## Setup and Installation

### Prerequisites

- Python 3.8+
- pip (Python package manager)

### Installation Steps

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd BookApi
   ```

2. Create and activate a virtual environment (optional but recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up environment variables (copy .env.example to .env and modify as needed):
   ```bash
   cp .env.example .env
   ```

5. Run migrations to create the database:
   ```bash
   python manage.py migrate
   ```

6. Create a superuser (for API authentication):
   ```bash
   python manage.py createsuperuser
   ```

7. Run the development server:
   ```bash
   python manage.py runserver
   ```

## API Documentation

The API is fully documented using Swagger and ReDoc. Once the server is running, you can access:

- **Swagger UI**: [http://localhost:8000/swagger/](http://localhost:8000/swagger/)
- **ReDoc**: [http://localhost:8000/redoc/](http://localhost:8000/redoc/)
- **API Schema**: [http://localhost:8000/swagger.json](http://localhost:8000/swagger.json)

These interactive documentation pages allow you to:
- Explore all available endpoints
- See request/response formats
- Test API calls directly from the browser
- Understand authentication requirements

## API Endpoints

### Books

- **List all books**: `GET /books/api/books/`
- **Create a new book**: `POST /books/api/books/`
- **Retrieve a specific book**: `GET /books/api/books/{slug}/`
- **Update a book**: `PUT /books/api/books/{slug}/`
- **Partially update a book**: `PATCH /books/api/books/{slug}/`
- **Delete a book**: `DELETE /books/api/books/{slug}/`
- **Get book reviews**: `GET /books/api/books/{slug}/reviews/`

### Authors

- **List all authors**: `GET /books/api/authors/`
- **Create a new author**: `POST /books/api/authors/`
- **Retrieve a specific author**: `GET /books/api/authors/{id}/`
- **Update an author**: `PUT /books/api/authors/{id}/`
- **Partially update an author**: `PATCH /books/api/authors/{id}/`
- **Delete an author**: `DELETE /books/api/authors/{id}/`

### Publishers

- **List all publishers**: `GET /books/api/publishers/`
- **Create a new publisher**: `POST /books/api/publishers/`
- **Retrieve a specific publisher**: `GET /books/api/publishers/{id}/`
- **Update a publisher**: `PUT /books/api/publishers/{id}/`
- **Partially update a publisher**: `PATCH /books/api/publishers/{id}/`
- **Delete a publisher**: `DELETE /books/api/publishers/{id}/`

### Reviews

- **List all reviews**: `GET /books/api/reviews/`
- **Create a new review**: `POST /books/api/reviews/`
- **Retrieve a specific review**: `GET /books/api/reviews/{id}/`
- **Update a review**: `PUT /books/api/reviews/{id}/`
- **Partially update a review**: `PATCH /books/api/reviews/{id}/`
- **Delete a review**: `DELETE /books/api/reviews/{id}/`

### Authentication

- **Login (Browser)**: `GET /api-auth/login/`
- **Get auth token**: `POST /api-token-auth/`

## Authentication

The API uses token-based authentication. To authenticate:

1. Obtain a token by sending a POST request to `/api-token-auth/` with your username and password:
   ```json
   {
     "username": "your_username",
     "password": "your_password"
   }
   ```

2. Include the token in the Authorization header of your requests:
   ```
   Authorization: Token your_token_here
   ```

## Permissions

- **GET** requests (list and retrieve) are allowed for all users (authenticated or not)
- **POST**, **PUT**, **PATCH**, and **DELETE** requests require authentication

## Filtering and Searching

The API supports various filtering and searching options:

- **Search books**: `GET /books/api/books/?search=django`
- **Filter books by language**: `GET /books/api/books/?language=en`
- **Filter books by genre**: `GET /books/api/books/?genre=fiction`
- **Order books by rating**: `GET /books/api/books/?ordering=-rating`
- **Search authors by name**: `GET /books/api/authors/?search=tolkien`
- **Filter reviews by rating**: `GET /books/api/reviews/?rating=5`

## Example Usage

### Get all books
```bash
curl -X GET http://localhost:8000/books/api/books/
```

### Get a specific book by slug
```bash
curl -X GET http://localhost:8000/books/api/books/django-for-beginners/
```

### Create a new book (requires authentication)
```bash
curl -X POST http://localhost:8000/books/api/books/ \
  -H "Authorization: Token your_token_here" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Django for Beginners",
    "author": 1,
    "published_date": "2020-01-01",
    "isbn": "1234567890123",
    "pages": 300,
    "language": "en",
    "genre": "non_fiction",
    "description": "A beginner-friendly guide to Django"
  }'
```

### Get all reviews for a specific book
```bash
curl -X GET http://localhost:8000/books/api/books/django-for-beginners/reviews/
```

## Development

### Running Tests
```bash
python manage.py test
```

### Code Style
This project follows PEP 8 style guidelines. You can check your code with:
```bash
flake8
```

## License

This project is licensed under the MIT License - see the LICENSE file for details.
