from datetime import date

from django.core.exceptions import ValidationError
from django.test import TestCase
from django.utils.text import slugify

from books.models import Book


class BookModelTests(TestCase):
    """
    Test cases for the Book model.
    """

    def setUp(self):
        """
        Set up test data.
        """
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

    def test_book_creation(self):
        """
        Test that a book can be created with valid data.
        """
        self.assertEqual(self.book.title, "Test Book")
        self.assertEqual(self.book.author, "Test Author")
        self.assertEqual(self.book.published_date, date(2020, 1, 1))
        self.assertEqual(self.book.isbn, "1234567890123")
        self.assertEqual(self.book.pages, 200)
        self.assertEqual(self.book.language, "en")
        self.assertEqual(self.book.genre, "fiction")
        self.assertEqual(self.book.description, "Test description")
        self.assertEqual(self.book.rating, 4.5)

    def test_slug_generation(self):
        """
        Test that a slug is automatically generated from the title.
        """
        self.assertEqual(self.book.slug, slugify(self.book.title))

    def test_custom_slug(self):
        """
        Test that a custom slug can be provided.
        """
        book = Book.objects.create(
            title="Custom Slug Book",
            slug="custom-slug",
            author="Test Author",
            published_date=date(2020, 1, 1),
            isbn="1234567890124",
            pages=200,
            language="en",
            genre="fiction",
        )
        self.assertEqual(book.slug, "custom-slug")

    def test_str_representation(self):
        """
        Test the string representation of a book.
        """
        self.assertEqual(str(self.book), "Test Book")

    def test_rating_validation(self):
        """
        Test that rating validation works correctly.
        """
        # Test valid ratings
        for rating in [0.0, 2.5, 5.0]:
            self.book.rating = rating
            self.book.full_clean()  # Should not raise ValidationError

        # Test invalid ratings
        for rating in [-1.0, 5.1, 6.0]:
            self.book.rating = rating
            with self.assertRaises(ValidationError):
                self.book.full_clean()

    def test_unique_isbn(self):
        """
        Test that ISBN must be unique.
        """
        with self.assertRaises(Exception):
            Book.objects.create(
                title="Another Book",
                author="Another Author",
                published_date=date(2021, 1, 1),
                isbn="1234567890123",  # Same ISBN as self.book
                pages=300,
                language="en",
                genre="fiction",
            )

    def test_book_ordering(self):
        """
        Test that books are ordered by published_date in descending order.
        """
        book2 = Book.objects.create(
            title="Newer Book",
            author="Test Author",
            published_date=date(2021, 1, 1),
            isbn="1234567890125",
            pages=200,
            language="en",
            genre="fiction",
        )

        books = Book.objects.all()
        self.assertEqual(books[0], book2)  # Newer book should come first
        self.assertEqual(books[1], self.book)
