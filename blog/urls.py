from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.blogHome, name='blogHome'),
    path('postblog', views.postblog, name='postblog'),
    path('like', views.like_post, name='like_post'),
    path('<str:slug>', views.blogPost, name='blogPost')
]