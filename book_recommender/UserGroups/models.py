from django.db import models
from Users.models import *
from Books.models import *
from django.utils import timezone
import os
from django.contrib.auth.models import User
from django.conf import settings

def get_image_path(instance, filename):
    return os.path.join('UserGroups/media/', str(instance.id), filename)

# Create your models here.
class Message(models.Model):
    message_text = models.CharField(max_length=2000)
    sender_id = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    group_id = models.ForeignKey('UserGroups.UserGroup',on_delete=models.CASCADE)
    sent_on = models.DateTimeField(default=timezone.now)


    def __str__(self):
        return  self.message_text

class UserGroup(models.Model):
    group_name = models.CharField(max_length=200)
    group_description = models.TextField(blank=True)
    group_pic = models.ImageField(upload_to=get_image_path, blank=True, null=True)
    group_genre = models.ManyToManyField(Genre, blank=True)
    group_creator = models.ForeignKey(User, related_name='owner', on_delete=models.CASCADE)
    group_books = models.ManyToManyField(Book, blank=True)
    group_members = models.ManyToManyField(User, related_name='my_groups', blank=True)
    # group_user = models.ManyToManyField(settings.AUTH_USER_MODEL)
    # book_title = models.CharField(max_length = 1000)
    # book_publisher = models.CharField(max_length = 1000, blank = True)
    # book_genre = models.ManyToManyField(Genre, blank = True)
    # book_description = models.TextField(blank = True)
    # published_at = models.TextField()
    # book_cover = models.TextField(max_length = 1000)
    # book_author = models.CharField(max_length= 100)

    def __str__(self):
        return self.group_name
