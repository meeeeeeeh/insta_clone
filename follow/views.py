from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from .models import Follow
from post.models import Stream
from django.contrib.auth.models import User
from post.models import Post


def follow_user(request, username):
    following = get_object_or_404(User, username=username)
    follow = Follow(follower=request.user, following=following)
    follow.save()
    posts = Post.objects.all().filter(user=following)[:10]
    for post in posts:
        stream = Stream(user=request.user, post=post, date=post.posted, following=following)
        stream.save()
    return redirect(reverse('authentification:profile', args=[username]))


def unfollow_user(request, username):
    following = get_object_or_404(User, username=username)
    Follow.objects.filter(follower=request.user, following = following).delete()
    Stream.objects.filter(following=following, user=request.user).all().delete()
    return redirect(reverse('authentification:profile', args=[username]))
