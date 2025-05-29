# Book API

A RESTful API for managing books built with Django and Django Rest Framework.

## Setup

1. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

2. Run migrations:
   ```
   python manage.py migrate
   ```

3. Create a superuser (for API authentication):
   ```
   python manage.py createsuperuser
   ```

4. Run the development server:
   ```
   python manage.py runserver
   ```

## API Endpoints

### Books

- **List all books**: `GET /books/api/books/`
- **Create a new book**: `POST /books/api/books/`
- **Retrieve a specific book**: `GET /books/api/books/{id}/`
- **Update a book**: `PUT /books/api/books/{id}/`
- **Partially update a book**: `PATCH /books/api/books/{id}/`
- **Delete a book**: `DELETE /books/api/books/{id}/`

### Authentication

- **Login (Browser)**: `GET /api-auth/login/`
- **Get auth token**: `POST /api-token-auth/`
  - Requires username and password in the request body
  - Returns a token that can be used in the Authorization header

## Authentication

The API uses token-based authentication. To authenticate:

1. Obtain a token by sending a POST request to `/api-token-auth/` with your username and password.
2. Include the token in the Authorization header of your requests:
   ```
   Authorization: Token your_token_here
   ```

## Permissions

- **GET** requests (list and retrieve) are allowed for all users (authenticated or not)
- **POST**, **PUT**, **PATCH**, and **DELETE** requests require authentication

## Example Usage

### Get all books
```
curl -X GET http://localhost:8000/books/api/books/
```

### Create a new book (requires authentication)
```
curl -X POST http://localhost:8000/books/api/books/ \
  -H "Authorization: Token your_token_here" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Django for Beginners",
    "author": "William S. Vincent",
    "published_date": "2020-01-01",
    "isbn": "1234567890123",
    "pages": 300,
    "language": "en"
  }'
```