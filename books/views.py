from django.http import HttpResponse
from django.shortcuts import render
from rest_framework import viewsets, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend

from books.models import Book, Author, Publisher, Review
from books.serializers import (
    BookSerializer, BookListSerializer, AuthorSerializer, 
    PublisherSerializer, ReviewSerializer
)


# Create your views here.
def home(request):
    """
    View function for the home page of the site.

    Displays a list of all books with their authors.

    Args:
        request: The HTTP request object

    Returns:
        Rendered HTML template with the list of books
    """
    books = Book.objects.select_related('author').all()
    return render(request, 'home.html', {'books': books})


class AuthorViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows authors to be viewed or edited.

    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.

    Supports filtering by name using the search parameter.

    Example:
        GET /books/api/authors/?search=tolkien
    """
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    search_fields = ['name']


class PublisherViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows publishers to be viewed or edited.

    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.

    Supports filtering by name using the search parameter.

    Example:
        GET /books/api/publishers/?search=penguin
    """
    queryset = Publisher.objects.all()
    serializer_class = PublisherSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']


class BookViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows books to be viewed or edited.

    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.

    Additional actions:
    - `reviews`: Get all reviews for a specific book

    Supports:
    - Searching by title, author name, or ISBN
    - Filtering by language, genre, or published date
    - Ordering by title, published date, or rating

    Examples:
        GET /books/api/books/?search=django
        GET /books/api/books/?language=en&genre=fiction
        GET /books/api/books/?ordering=-rating
        GET /books/api/books/{slug}/reviews/
    """
    queryset = Book.objects.select_related('author', 'publisher').prefetch_related('reviews').all()
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [filters.SearchFilter, DjangoFilterBackend, filters.OrderingFilter]
    search_fields = ['title', 'author__name', 'isbn']
    filterset_fields = ['language', 'genre', 'published_date']
    ordering_fields = ['title', 'published_date', 'rating']
    ordering = ['-published_date']
    lookup_field = 'slug'

    def get_serializer_class(self):
        """
        Return different serializers based on the action.

        For list views, return a simplified serializer.
        For all other actions, return the full serializer.

        Returns:
            Serializer class: BookListSerializer for list action, BookSerializer otherwise
        """
        if self.action == 'list':
            return BookListSerializer
        return BookSerializer

    @action(detail=True, methods=['get'])
    def reviews(self, request, slug=None):
        """
        Retrieve all reviews for a specific book.

        Args:
            request: The HTTP request object
            slug: The slug of the book to retrieve reviews for

        Returns:
            Response: A list of all reviews for the specified book

        Example:
            GET /books/api/books/django-for-beginners/reviews/
        """
        book = self.get_object()
        reviews = book.reviews.all()
        serializer = ReviewSerializer(reviews, many=True)
        return Response(serializer.data)


class ReviewViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows reviews to be viewed or edited.

    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.

    Supports filtering by book or rating.

    Examples:
        GET /books/api/reviews/?book=1
        GET /books/api/reviews/?rating=5
    """
    queryset = Review.objects.select_related('book').all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['book', 'rating']
