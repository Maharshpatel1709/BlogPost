from django.db import models
from django.contrib.auth.models import User
from blog.models import Post

# Create your models here.

class Users(models.Model):
    sNo = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    uname = models.CharField(max_length=100)
    name = models.CharField(max_length=255)
    email = models.CharField(max_length=100)
    about = models.TextField()
    followers = models.ManyToManyField(User, related_name='followers', blank=True)
    following = models.ManyToManyField(User, related_name='following', blank=True)
    blogs = models.ManyToManyField(Post, related_name='blogs', blank=True)
    likes = models.IntegerField(default=0)

    def __str__(self):
        return self.uname + ' - ' + self.name
    
    def followers_count(self):
        return self.followers.count()
    
    def following_count(self):
        return self.following.count()
    
    def blogs_count(self):
        return self.blogs.count()

class Contact(models.Model):
    sNo = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=13)
    email = models.CharField(max_length=100)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True, blank=True)

    def __str__(self):
        return self.name + ' - ' + self.email