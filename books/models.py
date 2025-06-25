from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.text import slugify

# Available language choices for books
LANGUAGE_CHOICES = (
    ("en", "English"),
    ("es", "Spanish"),
    ("fr", "French"),
    ("de", "German"),
    ("it", "Italian"),
    ("pt", "Portuguese"),
    ("zh", "Chinese"),
    ("ja", "Japanese"),
    ("ru", "Russian"),
)

# Available genre choices for books
GENRE_CHOICES = (
    ("fiction", "Fiction"),
    ("non_fiction", "Non-Fiction"),
    ("sci_fi", "Science Fiction"),
    ("fantasy", "Fantasy"),
    ("mystery", "Mystery"),
    ("thriller", "Thriller"),
    ("romance", "Romance"),
    ("biography", "Biography"),
    ("history", "History"),
    ("self_help", "Self Help"),
    ("other", "Other"),
)


# Author and Publisher models will be added in a later migration


class Book(models.Model):
    """
    Model representing a book.

    A book is associated with one author and optionally one publisher.
    It can have multiple reviews associated with it through the 'reviews' related name.
    """

    title = models.CharField(max_length=200, help_text="The title of the book")
    slug = models.SlugField(
        max_length=250,
        blank=True,
        help_text="URL-friendly version of the title (auto-generated)",
    )
    author = models.CharField(max_length=100, help_text="The author's name")
    # publisher field will be added in a later migration
    published_date = models.DateField(help_text="The date when the book was published")
    isbn = models.CharField(
        max_length=13,
        unique=True,
        help_text="International Standard Book Number (13 digits)",
    )
    pages = models.IntegerField(
        # validators=[MinValueValidator(1)],
        help_text="Number of pages in the book"
    )
    cover_image = models.URLField(
        blank=True, null=True, help_text="URL to the book's cover image"
    )
    language = models.CharField(
        max_length=30,
        choices=LANGUAGE_CHOICES,
        default="en",
        help_text="The primary language of the book",
    )
    genre = models.CharField(
        max_length=30,
        choices=GENRE_CHOICES,
        default="fiction",
        help_text="The genre or category of the book",
    )
    description = models.TextField(
        blank=True, null=True, help_text="A summary or description of the book"
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True,
        help_text="The retail price of the book",
    )
    rating = models.DecimalField(
        max_digits=3,
        decimal_places=1,
        blank=True,
        null=True,
        validators=[MinValueValidator(0.0), MaxValueValidator(5.0)],
        help_text="Average rating of the book (0-5)",
    )
    created_at = models.DateTimeField(
        auto_now_add=True, help_text="When the book record was created"
    )
    updated_at = models.DateTimeField(
        auto_now=True, help_text="When the book record was last updated"
    )

    class Meta:
        ordering = ["-published_date"]
        indexes = [
            models.Index(fields=["title"]),
            models.Index(fields=["isbn"]),
            models.Index(fields=["published_date"]),
            models.Index(fields=["genre"]),
        ]

    def save(self, *args, **kwargs):
        """
        Override the save method to automatically generate a slug from the title
        if one is not provided.
        """
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title
