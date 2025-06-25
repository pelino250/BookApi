from django.test import TestCase
from django.urls import resolve, reverse
from rest_framework.test import APITestCase

from books.views import home


class UrlsTests(TestCase):
    """
    Test cases for URL routing.
    """

    def test_home_url_resolves(self):
        """
        Test that the home URL resolves to the home view.
        """
        url = reverse("home")
        self.assertEqual(url, "/home/")
        resolver = resolve(url)
        self.assertEqual(resolver.func, home)


class ApiUrlsTests(APITestCase):
    """
    Test cases for API URL routing.
    """

    def test_book_list_url_resolves(self):
        """
        Test that the book-list URL resolves to the BookViewSet list action.
        """
        url = reverse("book-list")
        self.assertEqual(url, "/api/v1/books/")

    def test_book_detail_url_resolves(self):
        """
        Test that the book-detail URL resolves to the BookViewSet retrieve action.
        """
        url = reverse("book-detail", kwargs={"slug": "test-book"})
        self.assertEqual(url, "/api/v1/books/test-book/")

    def test_book_featured_url_resolves(self):
        """
        Test that the book-featured URL resolves to the BookViewSet featured action.
        """
        url = reverse("book-featured")
        self.assertEqual(url, "/api/v1/books/featured/")

    def test_book_by_genre_url_resolves(self):
        """
        Test that the book-by-genre URL resolves to the BookViewSet by_genre action.
        """
        url = reverse("book-by-genre", kwargs={"genre_name": "fiction"})
        self.assertEqual(url, "/api/v1/books/genre/fiction/")

    def test_api_token_url_resolves(self):
        """
        Test that the api-token URL resolves correctly.
        """
        url = reverse("api-token")
        self.assertEqual(url, "/api/token/")
