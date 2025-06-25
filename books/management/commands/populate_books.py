import random
from datetime import datetime, timedelta
from decimal import Decimal

from django.core.management.base import BaseCommand
from django.utils import timezone
from faker import Faker

from books.models import Book, LANGUAGE_CHOICES, GENRE_CHOICES


class Command(BaseCommand):
    help = "Populates the database with dummy book data"

    def add_arguments(self, parser):
        parser.add_argument(
            "--count",
            type=int,
            default=10,
            help="Number of books to create (default: 10)",
        )

    def handle(self, *args, **options):
        count = options["count"]
        fake = Faker()

        self.stdout.write(
            self.style.SUCCESS(f"Starting to create {count} dummy books...")
        )

        # Generate a list of unique ISBNs to avoid unique constraint violations
        existing_isbns = set(Book.objects.values_list("isbn", flat=True))

        # Create dummy books
        for i in range(count):
            # Generate a unique ISBN
            isbn = None
            while isbn is None or isbn in existing_isbns:
                isbn = "".join([str(random.randint(0, 9)) for _ in range(13)])
            existing_isbns.add(isbn)

            # Generate random published date (within the last 20 years)
            published_date = fake.date_between(start_date="-20y", end_date="today")

            # Generate random language and genre
            language = random.choice([lang[0] for lang in LANGUAGE_CHOICES])
            genre = random.choice([g[0] for g in GENRE_CHOICES])

            # Generate random rating between 0 and 5 with one decimal place
            rating = None
            if random.choice([True, False]):  # 50% chance of having a rating
                rating = Decimal(str(round(random.uniform(0, 5), 1)))

            # Generate random price between $5 and $50
            price = None
            if random.choice([True, False]):  # 50% chance of having a price
                price = Decimal(str(round(random.uniform(5, 50), 2)))

            # Create the book
            book = Book.objects.create(
                title=fake.catch_phrase(),
                author=fake.name(),
                published_date=published_date,
                isbn=isbn,
                pages=random.randint(50, 1000),
                cover_image=(
                    f"https://picsum.photos/id/{random.randint(1, 1000)}/200/300"
                    if random.choice([True, False])
                    else None
                ),
                language=language,
                genre=genre,
                description=(
                    fake.paragraph(nb_sentences=5)
                    if random.choice([True, False])
                    else None
                ),
                price=price,
                rating=rating,
            )

            self.stdout.write(self.style.SUCCESS(f"Created book: {book.title}"))

        self.stdout.write(
            self.style.SUCCESS(f"Successfully created {count} dummy books!")
        )
