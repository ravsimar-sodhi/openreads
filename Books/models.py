from django.db import models
from django.utils import timezone

class Genres(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self):
        return  self.name

class Books(models.Model):
    book_title = models.CharField(max_length = 1000)
    book_publisher = models.CharField(max_length = 1000)
    book_genre = models.ManyToManyField(Genres)
    book_description = models.TextField()
    published_at = models.TextField()
    book_cover = models.TextField(max_length = 1000)
    book_author = models.CharField(max_length= 100)

    def __str__(self):
        return self.book_title

