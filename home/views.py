from django.shortcuts import render, HttpResponse, redirect
from django.http.response import HttpResponseRedirect
from django.urls import reverse
from .models import Contact, Users
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

# Create your views here.

def home(request):
    return render(request, 'home/home.html')

def about(request):
    return render(request, 'home/about.html')

def contact(request):
    if request.method=='POST':
        name = request.POST['name']
        email = request.POST['email']
        phone = request.POST['phone']
        content = request.POST['content']

        if len(name)<2 or len(email)<3 or len(phone)<10 or len(content)<4:
            messages.error(request, "Please fill the form correctly")
        else:
            contact=Contact(name=name, email=email, phone=phone, content=content)
            contact.save()
            messages.success(request, "Your message has been successfully sent")

    return render(request, 'home/contact.html') 

def handleSignup(request):
    if request.method == 'POST':
        username = request.POST['username']
        name = request.POST['name']
        email = request.POST['email']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']

        if len(username) > 20:
            messages.error(request, " Your username must be under 10 characters")
            return redirect('home')

        if not username.isalnum():
            messages.error(request, " Username should only contain letters and numbers")
            return redirect('home')

        if pass1 != pass2:
            messages.error(request, "Passwords do not match")
            return redirect('home')

        myuser = User.objects.create_user(username, email, pass1)
        myuser.name = name
        myuser.save()

        user_id = User.objects.get(username=username)

        users=Users(uname=username, name=name, email=email, user_id=user_id)
        users.save()

        messages.success(request, "Your BlogPost account has been created successfully!")
        return redirect('home')   

    else:
        return HttpResponse('404 - Not Found')

def handleLogin(request):
    if request.method == 'POST':
        loginusername = request.POST['loginusername']
        loginpass = request.POST['loginpass']

        user = authenticate(username=loginusername, password=loginpass)

        if user is not None:
            login(request, user)
            messages.success(request, "Successfully Logged In")
            return redirect('home')
        else:
            messages.error(request, "Invalid Credentials, Please try again")
            return redirect('home')

    else:
        return HttpResponse('404 - Not Found')

@login_required
def handleLogout(request):
    logout(request)
    messages.success(request, "Successfully Logged Out")
    return redirect('home')

@login_required
def profile(request, uname):
    users = Users.objects.filter(uname=uname).first()
    
    not_self = False
    if users.user_id.id != request.user.id:
        not_self = True
    
    blogs = users.blogs.order_by('-timestamp')
    
    is_follower = False
    if users.followers.filter(id=request.user.id).exists():
        is_follower = True

    context = {'users': users, 'blogs': blogs, 'not_self': not_self, 'is_follower': is_follower, 'posts': users.blogs_count(), 'followers': users.followers_count(), 'following': users.following_count()}
    return render(request, 'home/profile.html', context)

@login_required
def follow(request):
    other_user_id = request.POST['user_id']
    other_user = Users.objects.get(sNo=other_user_id)

    curr_user = Users.objects.get(user_id=request.user.id)

    if other_user.followers.filter(id=request.user.id).exists():
        other_user.followers.remove(request.user)
        curr_user.following.remove(User.objects.get(username=other_user.uname))
    else:
        other_user.followers.add(request.user)
        curr_user.following.add(User.objects.get(username=other_user.uname))
    
    return HttpResponseRedirect(reverse('profile', args=[str(other_user.uname)]))