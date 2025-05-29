from rest_framework import serializers
from .models import Book, Author, Publisher, Review


class AuthorSerializer(serializers.ModelSerializer):
    """
    Serializer for the Author model.

    Provides a complete representation of an author with all fields.
    """
    class Meta:
        model = Author
        fields = ['id', 'name', 'biography', 'birth_date', 'website']


class PublisherSerializer(serializers.ModelSerializer):
    """
    Serializer for the Publisher model.

    Provides a complete representation of a publisher with all fields.
    """
    class Meta:
        model = Publisher
        fields = ['id', 'name', 'website', 'address']


class ReviewSerializer(serializers.ModelSerializer):
    """
    Serializer for the Review model.

    Provides a complete representation of a review with all fields.
    The created_at field is read-only as it's automatically set when a review is created.
    """
    class Meta:
        model = Review
        fields = ['id', 'book', 'user_name', 'rating', 'comment', 'created_at']
        read_only_fields = ['created_at']


class BookSerializer(serializers.ModelSerializer):
    """
    Serializer for the Book model.

    Provides a detailed representation of a book with all fields, including:
    - Nested author details
    - Nested publisher details
    - All associated reviews
    - Calculated average rating

    The slug, created_at, and updated_at fields are read-only as they're automatically generated.
    """
    # Nested serializers for related objects
    author_details = AuthorSerializer(source='author', read_only=True)
    publisher_details = PublisherSerializer(source='publisher', read_only=True)
    reviews = ReviewSerializer(many=True, read_only=True)

    # Calculated field
    average_rating = serializers.SerializerMethodField()

    class Meta:
        model = Book
        fields = [
            'id', 'title', 'slug', 'author', 'author_details', 
            'publisher', 'publisher_details', 'published_date', 
            'isbn', 'pages', 'cover_image', 'language', 'genre',
            'description', 'price', 'rating', 'reviews', 
            'average_rating', 'created_at', 'updated_at'
        ]
        read_only_fields = ['slug', 'created_at', 'updated_at']

    def get_average_rating(self, obj):
        """
        Calculate the average rating for a book based on its reviews.

        Returns:
            float: The average rating or None if there are no reviews.
        """
        reviews = obj.reviews.all()
        if reviews:
            return sum(review.rating for review in reviews) / len(reviews)
        return None


class BookListSerializer(serializers.ModelSerializer):
    """
    Simplified serializer for the Book model used in list views.

    Provides a condensed representation of a book with only essential fields,
    including the author's name instead of just the ID.
    """
    # Get the author's name instead of just the ID
    author_name = serializers.CharField(source='author.name', read_only=True)

    class Meta:
        model = Book
        fields = [
            'id', 'title', 'slug', 'author_name', 'published_date', 
            'isbn', 'genre', 'rating'
        ]
