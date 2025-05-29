from django.contrib import admin
from django.utils.html import format_html

from books.models import Book


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'published_date', 'isbn', 'language', 'genre', 'display_rating']
    list_filter = ['language', 'genre', 'published_date']
    search_fields = ['title', 'author', 'isbn', 'description']
    readonly_fields = ['created_at', 'updated_at', 'slug']
    fieldsets = [
        (None, {'fields': ['title', 'slug', 'author']}),
        ('Book Details', {'fields': ['published_date', 'isbn', 'pages', 'language', 'genre', 'description']}),
        ('Media and Pricing', {'fields': ['cover_image', 'price', 'rating']}),
        ('Metadata', {'fields': ['created_at', 'updated_at'], 'classes': ['collapse']}),
    ]

    def display_rating(self, obj):
        if obj.rating:
            return f"{obj.rating}/5.0"
        return '-'

    display_rating.short_description = 'Rating'


# Author, Publisher, and Review admin classes will be added back later
