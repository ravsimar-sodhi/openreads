from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now
from django.db.models.signals import post_save
from Books.models import *

# class GroupMember(models.Model):
#     user = models.ForeignKey(User,on_delete=models.CASCADE)
#     group = models.ForeignKey('UserGroups.UserGroup',on_delete=models.CASCADE)

class rateList(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    book=models.ForeignKey('Books.Book',on_delete=models.CASCADE)
    Choices = (
        (1,  '*'),
        (2,  '**'),
        (3,  '***'),
        (4,  '****'),
        (5,  '*****'),
      )
    rate = models.IntegerField(default=1, choices=Choices)

class Bookshelf(models.Model):
  name = models.CharField(max_length=256,blank=False)
  user = models.ForeignKey(User, on_delete=models.CASCADE)
  book = models.ManyToManyField(Book, blank = True)
# Create your models here.
