from django.db import models


# Create your models here.
from django.utils import timezone

class Genre(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self):
        return  self.name

class Book(models.Model):
    book_title = models.CharField(max_length = 1000)
    book_publisher = models.CharField(max_length = 1000, blank = True)
    book_genre = models.ManyToManyField(Genre, blank = True)
    book_description = models.TextField(blank = True)
    published_at = models.TextField()
    book_cover = models.TextField(max_length = 1000)
    book_author = models.CharField(max_length= 100)

    def __str__(self):
        return self.book_title
