from django.contrib import admin
from Books.models import Book, Genre
# Register your models here.

class BookAdmin(admin.ModelAdmin):
    list_display = ['id', 'book_title', 'book_author', 'book_avg_rating', 'book_num_of_ratings']

admin.site.register(Book, BookAdmin)

admin.site.register(Genre)
