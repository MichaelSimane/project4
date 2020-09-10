from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator

import datetime

from .models import User, Post, Profile

def index(request):    
    post = Post.objects.all().order_by("time").reverse()
    #  post = Post.objects.all().order_by("time").reverse()
        
    return render(request, "network/post.html", {            
        "posts": post                       
    })
    

def newpost(request):
    user = User.objects.get(email=request.user.email)

    if request.method == 'POST':        
        post = Post()
        post.user = user
        post.posts = request.POST["newPost"]
        
        post.save()

        return HttpResponseRedirect(reverse("index"))

    return render(request, "network/index.html")  


def edit(request, post_id):   
    post = Post.objects.get(pk=post_id)
    
    if request.method == "POST":
        post.posts = request.POST["edit"]
        post.save()
        return HttpResponseRedirect(reverse('index'))

    return render(request, "network/post.html")


@login_required(login_url='login')
def like(request, post_id):
    post = Post.objects.get(pk=post_id)
    if request.user in post.like.all():
        post.like.remove(request.user)
        response = '<svg width="1em" height="1em" viewBox="0 0 16 16" class="bi bi-heart" fill="red" xmlns="http://www.w3.org/2000/svg"><path fill-rule="evenodd" d="M8 2.748l-.717-.737C5.6.281 2.514.878 1.4 3.053c-.523 1.023-.641 2.5.314 4.385.92 1.815 2.834 3.989 6.286 6.357 3.452-2.368 5.365-4.542 6.286-6.357.955-1.886.838-3.362.314-4.385C13.486.878 10.4.28 8.717 2.01L8 2.748zM8 15C-7.333 4.868 3.279-3.04 7.824 1.143c.06.055.119.112.176.171a3.12 3.12 0 0 1 .176-.17C12.72-3.042 23.333 4.867 8 15z"/></svg>'
    else:
        post.like.add(request.user)
        response = '<svg width="1em" height="1em" viewBox="0 0 16 16" class="bi bi-heart-fill" fill="red" xmlns="http://www.w3.org/2000/svg"><path fill-rule="evenodd" d="M8 1.314C12.438-3.248 23.534 4.735 8 15-7.534 4.736 3.562-3.248 8 1.314z"/></svg>'
    likes = post.like.count()
    result = {
        'html': response,
        'likes': likes
    }
    return JsonResponse({'result': result})


@login_required(login_url='login')
def user(request, username):
    try:
        user = User.objects.get(username=username)
        profile = Profile.objects.get(user=user)
        users_profile = Profile.objects.get(user=request.user)
    except:
        return render(request, 'network/profile.html', {"error": True})
    follower = profile.followers.count()
    following = profile.following.count()
    post = Post.objects.filter(user=user).order_by('-time')
    return render(request, "network/profile.html", {
        "user": user,
        "follower": follower,
        "following": following,
        'users_profile': users_profile,
        "posts": post
    })


@login_required(login_url='login')
def follow(request):
    if request.method == "POST":
        login_user = request.POST["user"]
        user = User.objects.get(username=login_user)
        profile = Profile.objects.get(user=request.user)
        if user in profile.following.all():
             profile.following.remove(user)
             profile.save()
        else:
            profile.following.add(user)
            profile.save()

        # add current user to  user's follower list
        profile = Profile.objects.get(user=user)
        if request.user in profile.followers.all():
            profile.followers.remove(request.user)
            profile.save()
        else:
            profile.followers.add(request.user)
            profile.save()
        return HttpResponseRedirect(reverse("user", kwargs={"username": login_user})) 


def following(request):
    following = Profile.objects.get(user=request.user).following.all()
    posts = Post.objects.filter(user__in=following).order_by('-time')
    paginator = Paginator(posts, 10)
    
    return render(request, "network/following.html", {
        "posts": posts
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        profile = Profile()
        profile.user = user
        profile.save()
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")
