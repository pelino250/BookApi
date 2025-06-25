from io import StringIO

from django.core.management import call_command
from django.test import TestCase

from books.models import Book


class PopulateBooksCommandTests(TestCase):
    """
    Test cases for the populate_books management command.
    """

    def test_command_output(self):
        """
        Test that the command outputs the expected messages.
        """
        out = StringIO()
        call_command("populate_books", count=2, stdout=out)
        self.assertIn("Starting to create 2 dummy books", out.getvalue())
        self.assertIn("Successfully created 2 dummy books", out.getvalue())

    def test_command_creates_books(self):
        """
        Test that the command creates the specified number of books.
        """
        # Check initial count
        initial_count = Book.objects.count()

        # Run command to create 5 books
        call_command("populate_books", count=5)

        # Check that 5 books were created
        self.assertEqual(Book.objects.count(), initial_count + 5)

    def test_command_creates_valid_books(self):
        """
        Test that the command creates books with valid data.
        """
        # Run command to create 3 books
        call_command("populate_books", count=3)

        # Get the created books
        books = Book.objects.all()

        # Check that each book has valid data
        for book in books:
            # Check required fields
            self.assertIsNotNone(book.title)
            self.assertIsNotNone(book.author)
            self.assertIsNotNone(book.published_date)
            self.assertIsNotNone(book.isbn)
            self.assertIsNotNone(book.pages)
            self.assertIsNotNone(book.language)
            self.assertIsNotNone(book.genre)

            # Check that ISBN is 13 characters
            self.assertEqual(len(book.isbn), 13)

            # Check that pages is a positive integer
            self.assertGreater(book.pages, 0)

            # Check that slug was generated
            self.assertIsNotNone(book.slug)

    def test_command_creates_unique_isbns(self):
        """
        Test that the command creates books with unique ISBNs.
        """
        # Run command to create 10 books
        call_command("populate_books", count=10)

        # Get all ISBNs
        isbns = Book.objects.values_list("isbn", flat=True)

        # Check that all ISBNs are unique
        self.assertEqual(len(isbns), len(set(isbns)))

    def test_command_with_custom_count(self):
        """
        Test that the command respects the count parameter.
        """
        # Test with different counts
        for count in [1, 3, 5]:
            # Clear existing books
            Book.objects.all().delete()

            # Run command with specific count
            call_command("populate_books", count=count)

            # Check that the correct number of books was created
            self.assertEqual(Book.objects.count(), count)
