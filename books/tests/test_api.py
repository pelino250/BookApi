from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from books.models import Book
from datetime import date


class BookAPITests(APITestCase):
    """
    Test cases for the Book API endpoints.
    """

    def setUp(self):
        """
        Set up test data.
        """
        # Create a test user
        self.user = User.objects.create_user(
            username="testuser", email="test@example.com", password="testpassword"
        )

        # Create test books
        self.book1 = Book.objects.create(
            title="Test Book 1",
            author="Test Author 1",
            published_date=date(2020, 1, 1),
            isbn="1234567890123",
            pages=200,
            language="en",
            genre="fiction",
            description="Test description 1",
            rating=4.5,
        )

        self.book2 = Book.objects.create(
            title="Test Book 2",
            author="Test Author 2",
            published_date=date(2021, 1, 1),
            isbn="1234567890124",
            pages=300,
            language="en",
            genre="sci_fi",
            description="Test description 2",
            rating=3.5,
        )

        # URLs
        self.books_url = reverse("book-list")
        self.book1_url = reverse("book-detail", kwargs={"slug": self.book1.slug})
        self.featured_url = reverse("book-featured")
        self.genre_url = reverse("book-by-genre", kwargs={"genre_name": "fiction"})

    def test_list_books(self):
        """
        Test retrieving a list of books.
        """
        response = self.client.get(self.books_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 2)

    def test_retrieve_book(self):
        """
        Test retrieving a specific book.
        """
        response = self.client.get(self.book1_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], "Test Book 1")

    def test_create_book_unauthenticated(self):
        """
        Test that unauthenticated users cannot create books.
        """
        data = {
            "title": "New Book",
            "author": "New Author",
            "published_date": "2022-01-01",
            "isbn": "1234567890125",
            "pages": 400,
            "language": "en",
            "genre": "fiction",
        }
        response = self.client.post(self.books_url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_book_authenticated(self):
        """
        Test that authenticated users can create books.
        """
        self.client.force_authenticate(user=self.user)
        data = {
            "title": "New Book",
            "author": "New Author",
            "published_date": "2022-01-01",
            "isbn": "1234567890125",
            "pages": 400,
            "language": "en",
            "genre": "fiction",
        }
        response = self.client.post(self.books_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Book.objects.count(), 3)

    def test_featured_books(self):
        """
        Test retrieving featured books (rating >= 4.0).
        """
        response = self.client.get(self.featured_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 1)
        self.assertEqual(response.data["results"][0]["title"], "Test Book 1")

    def test_books_by_genre(self):
        """
        Test retrieving books by genre.
        """
        response = self.client.get(self.genre_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 1)
        self.assertEqual(response.data["results"][0]["title"], "Test Book 1")


class TokenAuthenticationTests(APITestCase):
    """
    Test cases for token creation and authentication.
    """

    def setUp(self):
        """
        Set up test data.
        """
        # Create a test user
        self.user = User.objects.create_user(
            username="tokenuser", email="token@example.com", password="tokenpassword"
        )

        # Create test book
        self.book = Book.objects.create(
            title="Token Test Book",
            author="Token Test Author",
            published_date=date(2022, 1, 1),
            isbn="9876543210123",
            pages=250,
            language="en",
            genre="mystery",
            description="Test description for token authentication",
            rating=4.0,
        )

        # URLs
        self.token_url = reverse("api-token")
        self.books_url = reverse("book-list")

    def test_obtain_token_valid_credentials(self):
        """
        Test obtaining a token with valid credentials.
        """
        data = {"username": "tokenuser", "password": "tokenpassword"}
        response = self.client.post(self.token_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("token", response.data)

        # Verify the token exists in the database
        token = response.data["token"]
        self.assertTrue(Token.objects.filter(key=token).exists())

    def test_obtain_token_invalid_credentials(self):
        """
        Test that invalid credentials do not generate a token.
        """
        data = {"username": "tokenuser", "password": "wrongpassword"}
        response = self.client.post(self.token_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertNotIn("token", response.data)

    def test_access_api_with_token(self):
        """
        Test accessing a protected API endpoint using a token.
        """
        # First, obtain a token
        token = Token.objects.create(user=self.user)

        # Create data for a new book
        data = {
            "title": "New Token Book",
            "author": "Token Author",
            "published_date": "2023-01-01",
            "isbn": "9876543210124",
            "pages": 300,
            "language": "en",
            "genre": "mystery",
        }

        # Try to create a book without authentication (should fail)
        response = self.client.post(self.books_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        # Add token to the request header
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {token.key}")

        # Try to create a book with token authentication (should succeed)
        response = self.client.post(self.books_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Book.objects.count(), 2)
        self.assertEqual(
            Book.objects.get(title="New Token Book").author, "Token Author"
        )
