from django.contrib import admin
from django.utils.html import format_html

from books.models import Book, Author, Publisher, Review


class ReviewInline(admin.TabularInline):
    model = Review
    extra = 0
    readonly_fields = ['created_at']


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ['title', 'author_name', 'publisher_name', 'published_date', 'isbn', 'language', 'genre', 'display_rating']
    list_filter = ['language', 'genre', 'published_date', 'publisher']
    search_fields = ['title', 'author__name', 'isbn', 'description']
    readonly_fields = ['created_at', 'updated_at', 'slug']
    autocomplete_fields = ['author', 'publisher']
    fieldsets = [
        (None, {'fields': ['title', 'slug', 'author', 'publisher']}),
        ('Book Details', {'fields': ['published_date', 'isbn', 'pages', 'language', 'genre', 'description']}),
        ('Media and Pricing', {'fields': ['cover_image', 'price', 'rating']}),
        ('Metadata', {'fields': ['created_at', 'updated_at'], 'classes': ['collapse']}),
    ]
    inlines = [ReviewInline]

    def author_name(self, obj):
        return obj.author.name

    def publisher_name(self, obj):
        return obj.publisher.name if obj.publisher else '-'

    def display_rating(self, obj):
        if obj.rating:
            return f"{obj.rating}/5.0"
        return '-'

    display_rating.short_description = 'Rating'
    author_name.short_description = 'Author'
    publisher_name.short_description = 'Publisher'


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ['name', 'birth_date', 'website_link', 'book_count']
    search_fields = ['name']
    readonly_fields = ['book_count']

    def website_link(self, obj):
        if obj.website:
            return format_html('<a href="{}" target="_blank">{}</a>', obj.website, obj.website)
        return '-'

    def book_count(self, obj):
        return obj.books.count()

    website_link.short_description = 'Website'
    book_count.short_description = 'Number of Books'


@admin.register(Publisher)
class PublisherAdmin(admin.ModelAdmin):
    list_display = ['name', 'website_link', 'book_count']
    search_fields = ['name']

    def website_link(self, obj):
        if obj.website:
            return format_html('<a href="{}" target="_blank">{}</a>', obj.website, obj.website)
        return '-'

    def book_count(self, obj):
        return obj.books.count()

    website_link.short_description = 'Website'
    book_count.short_description = 'Number of Books'


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['book_title', 'user_name', 'rating', 'created_at']
    list_filter = ['rating', 'created_at']
    search_fields = ['book__title', 'user_name', 'comment']
    readonly_fields = ['created_at']

    def book_title(self, obj):
        return obj.book.title

    book_title.short_description = 'Book'
