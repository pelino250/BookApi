from rest_framework import serializers
from .models import Book

# Author, Publisher, and Review serializers will be added back later


class BookSerializer(serializers.HyperlinkedModelSerializer):
    """
    Serializer for the Book model.

    Provides a detailed representation of a book with all fields.
    Includes hyperlinks to the book detail view for HATEOAS support.

    The slug, created_at, and updated_at fields are read-only as they're automatically generated.
    """

    url = serializers.HyperlinkedIdentityField(
        view_name="book-detail", lookup_field="slug"
    )

    class Meta:
        model = Book
        fields = [
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
        read_only_fields = ["slug", "created_at", "updated_at"]
        extra_kwargs = {"url": {"lookup_field": "slug"}}


class BookListSerializer(serializers.HyperlinkedModelSerializer):
    """
    Simplified serializer for the Book model used in list views.

    Provides a condensed representation of a book with only essential fields.
    Includes hyperlinks to the book detail view for HATEOAS support.
    """

    url = serializers.HyperlinkedIdentityField(
        view_name="book-detail", lookup_field="slug"
    )

    class Meta:
        model = Book
        fields = [
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
        extra_kwargs = {"url": {"lookup_field": "slug"}}
