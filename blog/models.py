from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Post(models.Model):
    sNo = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=100)
    slug = models.CharField(max_length=100)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True, blank=True)
    likes = models.ManyToManyField(User, related_name='likes', blank=True)

    def __str__(self):
        return self.title + ' - by - ' + self.author

    def total_likes(self):
        return self.likes.count()
