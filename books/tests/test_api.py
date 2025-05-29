from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase
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
            username='testuser',
            email='test@example.com',
            password='testpassword'
        )
        
        # Create test books
        self.book1 = Book.objects.create(
            title='Test Book 1',
            author='Test Author 1',
            published_date=date(2020, 1, 1),
            isbn='1234567890123',
            pages=200,
            language='en',
            genre='fiction',
            description='Test description 1',
            rating=4.5
        )
        
        self.book2 = Book.objects.create(
            title='Test Book 2',
            author='Test Author 2',
            published_date=date(2021, 1, 1),
            isbn='1234567890124',
            pages=300,
            language='en',
            genre='sci_fi',
            description='Test description 2',
            rating=3.5
        )
        
        # URLs
        self.books_url = reverse('book-list')
        self.book1_url = reverse('book-detail', kwargs={'slug': self.book1.slug})
        self.featured_url = reverse('book-featured')
        self.genre_url = reverse('book-by-genre', kwargs={'genre_name': 'fiction'})
    
    def test_list_books(self):
        """
        Test retrieving a list of books.
        """
        response = self.client.get(self.books_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)
    
    def test_retrieve_book(self):
        """
        Test retrieving a specific book.
        """
        response = self.client.get(self.book1_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Test Book 1')
    
    def test_create_book_unauthenticated(self):
        """
        Test that unauthenticated users cannot create books.
        """
        data = {
            'title': 'New Book',
            'author': 'New Author',
            'published_date': '2022-01-01',
            'isbn': '1234567890125',
            'pages': 400,
            'language': 'en',
            'genre': 'fiction'
        }
        response = self.client.post(self.books_url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_create_book_authenticated(self):
        """
        Test that authenticated users can create books.
        """
        self.client.force_authenticate(user=self.user)
        data = {
            'title': 'New Book',
            'author': 'New Author',
            'published_date': '2022-01-01',
            'isbn': '1234567890125',
            'pages': 400,
            'language': 'en',
            'genre': 'fiction'
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
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['title'], 'Test Book 1')
    
    def test_books_by_genre(self):
        """
        Test retrieving books by genre.
        """
        response = self.client.get(self.genre_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['title'], 'Test Book 1')