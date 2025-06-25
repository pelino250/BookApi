from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import (
    IsAuthenticatedOrReadOnly,
)
from rest_framework.response import Response

from books.models import Book
from books.serializers import BookListSerializer, BookSerializer


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
    books = Book.objects.all()
    return render(request, "home.html", {"books": books})


# Author and Publisher ViewSets will be added back later


class BookViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows books to be viewed or edited.

    list:
        Return a list of all books.

        Query parameters:
        - search: Search by title, author, or ISBN
        - language: Filter by language code (e.g., 'en', 'fr')
        - genre: Filter by genre (e.g., 'fiction', 'sci_fi')
        - published_date: Filter by publication date
        - ordering: Order results by specified field (e.g., 'title', '-rating')

    create:
        Create a new book.

    retrieve:
        Return the details of a specific book.

    update:
        Update all fields of a specific book.

    partial_update:
        Update one or more fields of a specific book.

    destroy:
        Delete a specific book.

    featured:
        Return a list of featured books (those with high ratings).

    by_genre:
        Return a list of books filtered by the specified genre.

    Examples:
        GET /api/v1/books/?search=django
        GET /api/v1/books/?language=en&genre=fiction
        GET /api/v1/books/?ordering=-rating
    """

    queryset = Book.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [
        filters.SearchFilter,
        DjangoFilterBackend,
        filters.OrderingFilter,
    ]
    search_fields = ["title", "author", "isbn"]
    filterset_fields = ["language", "genre", "published_date"]
    ordering_fields = ["title", "published_date", "rating"]
    ordering = ["-published_date"]
    lookup_field = "slug"

    def get_serializer_class(self):
        """
        Return different serializers based on the action.

        For list views, return a simplified serializer.
        For all other actions, return the full serializer.

        Returns:
            Serializer class: BookListSerializer for list action,
             BookSerializer otherwise
        """
        if self.action == "list":
            return BookListSerializer
        return BookSerializer

    def create(self, request, *args, **kwargs):
        """
        Create a new book with proper status code.

        Returns:
            Response: 201 Created on success with the created book data
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )

    def update(self, request, *args, **kwargs):
        """
        Update a book with proper status code.

        Returns:
            Response: 200 OK on success with the updated book data
        """
        partial = kwargs.pop("partial", False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        """
        Delete a book with proper status code.

        Returns:
            Response: 204 No Content on success
        """
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, methods=["get"])
    def featured(self, request):
        """
        Return a list of featured books (those with high ratings).

        Returns:
            Response: 200 OK with a list of featured books
        """
        featured_books = Book.objects.filter(rating__gte=4.0).order_by("-rating")
        page = self.paginate_queryset(featured_books)
        if page is not None:
            serializer = BookListSerializer(
                page, many=True, context={"request": request}
            )
            return self.get_paginated_response(serializer.data)
        serializer = BookListSerializer(
            featured_books, many=True, context={"request": request}
        )
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=["get"], url_path="genre/(?P<genre_name>[^/.]+)")
    def by_genre(self, request, genre_name=None):
        """
        Return a list of books filtered by the specified genre.

        Args:
            genre_name: The genre to filter by

        Returns:
            Response: 200 OK with a list of books in the specified genre
        """
        books = Book.objects.filter(genre=genre_name).order_by("-published_date")
        page = self.paginate_queryset(books)
        if page is not None:
            serializer = BookListSerializer(
                page, many=True, context={"request": request}
            )
            return self.get_paginated_response(serializer.data)
        serializer = BookListSerializer(books, many=True, context={"request": request})
        return Response(serializer.data, status=status.HTTP_200_OK)


# Review ViewSet will be added back later
