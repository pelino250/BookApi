from datetime import date

from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIRequestFactory

from books.models import Book
from books.serializers import BookListSerializer, BookSerializer


class BookSerializerTests(TestCase):
    """
    Test cases for the BookSerializer.
    """

    def setUp(self):
        """
        Set up test data.
        """
        self.factory = APIRequestFactory()
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
            price=19.99,
        )
        self.request = self.factory.get(
            reverse("book-detail", kwargs={"slug": self.book.slug})
        )

    def test_book_serializer_contains_expected_fields(self):
        """
        Test that the BookSerializer contains the expected fields.
        """
        serializer = BookSerializer(
            instance=self.book, context={"request": self.request}
        )
        data = serializer.data

        expected_fields = [
            "url",
            "id",
            "title",
            "slug",
            "author",
            "published_date",
            "isbn",
            "pages",
            "cover_image",
            "language",
            "genre",
            "description",
            "price",
            "rating",
            "created_at",
            "updated_at",
        ]

        self.assertEqual(set(data.keys()), set(expected_fields))

    def test_book_serializer_field_content(self):
        """
        Test that the BookSerializer correctly serializes the Book object.
        """
        serializer = BookSerializer(
            instance=self.book, context={"request": self.request}
        )
        data = serializer.data

        self.assertEqual(data["title"], "Test Book")
        self.assertEqual(data["author"], "Test Author")
        self.assertEqual(data["published_date"], "2020-01-01")
        self.assertEqual(data["isbn"], "1234567890123")
        self.assertEqual(data["pages"], 200)
        self.assertEqual(data["language"], "en")
        self.assertEqual(data["genre"], "fiction")
        self.assertEqual(data["description"], "Test description")
        self.assertEqual(float(data["rating"]), 4.5)
        self.assertEqual(float(data["price"]), 19.99)

    def test_book_serializer_validation(self):
        """
        Test that the BookSerializer correctly validates data.
        """
        # Valid data
        valid_data = {
            "title": "New Book",
            "author": "New Author",
            "published_date": "2022-01-01",
            "isbn": "9876543210123",
            "pages": 300,
            "language": "en",
            "genre": "fiction",
        }

        serializer = BookSerializer(data=valid_data, context={"request": self.request})
        self.assertTrue(serializer.is_valid())

        # Invalid data (missing required fields)
        invalid_data = {
            "title": "New Book",
            "author": "New Author",
            # missing published_date, isbn, pages
            "language": "en",
            "genre": "fiction",
        }

        serializer = BookSerializer(
            data=invalid_data, context={"request": self.request}
        )
        self.assertFalse(serializer.is_valid())
        self.assertIn("published_date", serializer.errors)
        self.assertIn("isbn", serializer.errors)
        self.assertIn("pages", serializer.errors)


class BookListSerializerTests(TestCase):
    """
    Test cases for the BookListSerializer.
    """

    def setUp(self):
        """
        Set up test data.
        """
        self.factory = APIRequestFactory()
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
        self.request = self.factory.get(reverse("book-list"))

    def test_book_list_serializer_contains_expected_fields(self):
        """
        Test that the BookListSerializer contains the expected fields.
        """
        serializer = BookListSerializer(
            instance=self.book, context={"request": self.request}
        )
        data = serializer.data

        expected_fields = [
            "url",
            "id",
            "title",
            "slug",
            "author",
            "published_date",
            "isbn",
            "genre",
            "rating",
        ]

        self.assertEqual(set(data.keys()), set(expected_fields))

        # Ensure detailed fields are not included
        detailed_fields = [
            "pages",
            "cover_image",
            "language",
            "description",
            "price",
            "created_at",
            "updated_at",
        ]
        for field in detailed_fields:
            self.assertNotIn(field, data)

    def test_book_list_serializer_field_content(self):
        """
        Test that the BookListSerializer correctly serializes the Book object.
        """
        serializer = BookListSerializer(
            instance=self.book, context={"request": self.request}
        )
        data = serializer.data

        self.assertEqual(data["title"], "Test Book")
        self.assertEqual(data["author"], "Test Author")
        self.assertEqual(data["published_date"], "2020-01-01")
        self.assertEqual(data["isbn"], "1234567890123")
        self.assertEqual(data["genre"], "fiction")
        self.assertEqual(float(data["rating"]), 4.5)
