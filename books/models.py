from django.db import models


LANGUAGE_CHOICES = (
    ('en', 'English'),
    ('es', 'Spanish'),
    ('fr', 'French'),
    ('de', 'German'),
    ('it', 'Italian'),
    ('pt', 'Portuguese'),
    ('zh', 'Chinese'),
    ('ja', 'Japanese'),
    ('ru', 'Russian'),
)
class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    published_date = models.DateField()
    isbn = models.CharField(max_length=13, unique=True)
    pages = models.IntegerField()
    cover_image = models.URLField(blank=True, null=True)
    language = models.CharField(
        max_length=30,
        choices=LANGUAGE_CHOICES,
        default='en'
    )

    def __str__(self):
        return self.title
