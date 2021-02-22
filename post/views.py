from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from .models import *
from django.views.generic import ListView, CreateView, DetailView
from django.contrib.auth.decorators import login_required


class HomeView(ListView):
    model = Post
    template_name = 'index.html'
    context_object_name = 'posts'


@login_required
def like(request, pk):
    user = request.user
    post = Post.objects.get(id=pk)
    current_likes = post.likes
    liked = Likes.objects.filter(user=user, post=post).count()
    if not liked:
        like = Likes.objects.create(user=user, post=post)
        current_likes += 1
    else:
        Likes.objects.filter(user=user, post=post).delete()
        current_likes -= 1
    post.likes = current_likes
    post.save()
    return redirect('post:post_detail', pk)


class PostDetailView(DetailView):
    model = Post
    template_name = "post_detail.html"
    context_object_name = "post"

