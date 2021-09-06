from blog.models import Post
from django.shortcuts import render, HttpResponse
from django.contrib.auth.decorators import login_required

# Create your views here.

@login_required
def blogHome(request):
    allPosts = Post.objects.all().order_by('-timestamp')
    context = {'allPosts': allPosts}
    return render(request, 'blog/blogHome.html', context)

@login_required
def blogPost(request, slug):
    post = Post.objects.filter(slug=slug).first()
    context = {'post': post}
    return render(request, 'blog/blogPost.html', context)
