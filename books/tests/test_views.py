from django.test import TestCase, Client
from django.urls import reverse
from books.models import Book
from datetime import date


class HomeViewTests(TestCase):
    """
    Test cases for the home view.
    """

    def setUp(self):
        """
        Set up test data.
        """
        self.client = Client()
        self.home_url = reverse("home")
        
        # Create test books
        self.book1 = Book.objects.create(
            title="Test Book 1",
            author="Test Author 1",
            published_date=date(2020, 1, 1),
            isbn="1234567890123",
            pages=200,
            language="en",
            genre="fiction",
        )
        
        self.book2 = Book.objects.create(
            title="Test Book 2",
            author="Test Author 2",
            published_date=date(2021, 1, 1),
            isbn="1234567890124",
            pages=300,
            language="en",
            genre="sci_fi",
        )

    def test_home_view_status_code(self):
        """
        Test that the home view returns a 200 status code.
        """
        response = self.client.get(self.home_url)
        self.assertEqual(response.status_code, 200)

    def test_home_view_template(self):
        """
        Test that the home view uses the correct template.
        """
        response = self.client.get(self.home_url)
        self.assertTemplateUsed(response, "home.html")

    def test_home_view_context(self):
        """
        Test that the home view passes the correct context to the template.
        """
        response = self.client.get(self.home_url)
        self.assertIn("books", response.context)
        self.assertEqual(len(response.context["books"]), 2)
        self.assertIn(self.book1, response.context["books"])
        self.assertIn(self.book2, response.context["books"])


class BookViewSetTests(TestCase):
    """
    Additional tests for the BookViewSet that aren't covered in test_api.py.
    """

    def setUp(self):
        """
        Set up test data.
        """
        self.client = Client()
        
        # Create test book
        self.book = Book.objects.create(
            title="Test Book",
            author="Test Author",
            published_date=date(2020, 1, 1),
            isbn="1234567890123",
            pages=200,
            language="en",
            genre="fiction",
            description="Test description",
            rating=4.5,
        )
        
        # URLs
        self.book_detail_url = reverse("book-detail", kwargs={"slug": self.book.slug})

    def test_book_detail_view_status_code(self):
        """
        Test that the book detail view returns a 200 status code.
        """
        response = self.client.get(self.book_detail_url)
        self.assertEqual(response.status_code, 200)

    def test_book_detail_view_data(self):
        """
        Test that the book detail view returns the correct data.
        """
        response = self.client.get(self.book_detail_url)
        self.assertEqual(response.data["title"], "Test Book")
        self.assertEqual(response.data["author"], "Test Author")
        self.assertEqual(response.data["isbn"], "1234567890123")
        self.assertEqual(response.data["rating"], 4.5)