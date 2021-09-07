from django.http.response import HttpResponseRedirect
from blog.models import Post
from django.shortcuts import get_object_or_404, render, HttpResponse, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.template.defaultfilters import slugify
from django.urls import reverse
# Create your views here.

@login_required
def blogHome(request):
    allPosts = Post.objects.all().order_by('-timestamp')
    context = {'allPosts': allPosts}
    return render(request, 'blog/blogHome.html', context)

@login_required
def blogPost(request, slug):
    post = Post.objects.filter(slug=slug).first()

    is_liked = False
    if post.likes.filter(id=request.user.id).exists():
        is_liked = True

    context = {'post': post, 'is_liked': is_liked, 'total_likes': post.total_likes()}
    return render(request, 'blog/blogPost.html', context)

def postblog(request):
    if request.method == 'POST':
        authorname = request.POST['authorname']
        blogtitle = request.POST['blogtitle']
        blogcontent = request.POST['blogcontent']
        slug = slugify(blogtitle)

        blogpost=Post(title=blogtitle, author=authorname, slug=slug, content=blogcontent)
        blogpost.save()
        messages.success(request, "Your Blog has been Posted Successfully")
        return redirect('home')   

    else:
        return HttpResponse('404 - Not Found')

def like_post(request):
    post_id = request.POST['post_id']
    post = Post.objects.get(sNo=post_id)
    slug = getattr(post, 'slug')
    is_liked = False
    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)
        is_liked = False
    else:
        post.likes.add(request.user)
        is_liked = True
    
    return HttpResponseRedirect(reverse('blogPost', args=[str(slug)]))