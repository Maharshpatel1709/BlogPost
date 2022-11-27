from django.http.response import HttpResponseRedirect
from blog.models import Post
from home.models import Users
from django.shortcuts import get_object_or_404, render, HttpResponse, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.template.defaultfilters import slugify
from django.urls import reverse
# Create your views here.

@login_required
def blogHome(request):
    user_following = Users.objects.get(user_id=request.user.id).sNo

    allPosts = Post.objects.raw('SELECT * FROM blog_post WHERE user_id_id in(SELECT user_id FROM home_users_following WHERE users_id = %s) ORDER BY timestamp DESC'%user_following)

    is_explore = False

    context = {'allPosts': allPosts, 'is_explore': is_explore}
    return render(request, 'blog/blogHome.html', context)

@login_required
def explore(request):
    allPosts = Post.objects.all().order_by('-timestamp')

    is_explore = True

    context = {'allPosts': allPosts, 'is_explore': is_explore}
    return render(request, 'blog/blogHome.html', context)

@login_required
def blogPost(request, sNo):
    post = Post.objects.get(sNo=sNo)

    uname = Users.objects.get(user_id=post.user_id).uname

    is_liked = False
    if post.likes.filter(id=request.user.id).exists():
        is_liked = True 
    print(is_liked)
    context = {'post': post, 'uname': uname, 'is_liked': is_liked, 'total_likes': post.total_likes()}
    return render(request, 'blog/blogPost.html', context)

@login_required
def postblog(request):
    if request.method == 'POST':
        # authorname = request.POST['authorname']
        blogtitle = request.POST['blogtitle']
        blogcontent = request.POST['blogcontent']
        slug = slugify(blogtitle)

        user_id = request.user.id
        users = Users.objects.get(user_id=user_id)

        authorname = users.name

        blogpost=Post(title=blogtitle, author=authorname, user_id=request.user, slug=slug, content=blogcontent)
        blogpost.save()

        
        users.blogs.add(blogpost)

        messages.success(request, "Your Blog has been Posted Successfully")
        return redirect('home')   

    else:
        return HttpResponse('404 - Not Found')

@login_required
def like_post(request):
    post_id = request.POST['post_id']
    post = Post.objects.get(sNo=post_id)

    users = Users.objects.get(user_id=post.user_id)

    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)
        users.likes -= 1
        users.save()
    else:
        post.likes.add(request.user)
        users.likes += 1
        users.save()
    
    return HttpResponseRedirect(reverse('blogPost', args=[str(post.sNo)]))