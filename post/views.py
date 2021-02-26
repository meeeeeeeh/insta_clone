from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from .models import *
from .forms import NewPostForm
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


class CreatePost(CreateView):
    model = Post
    form_class = NewPostForm
    template_name = "post_create.html"

    def form_valid(self, form):
        if self.request.user.is_authenticated:
            form.instance.user = self.request.user
        return super(CreatePost, self).form_valid(form)

    def form_invalid(self, form):
        print(form.errors)
        return redirect(reverse_lazy('post:post_create'))

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        self.object = None
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)



    def get_success_url(self, **kwargs):
        return reverse_lazy('authentification:profile', kwargs={'username': self.request.user.username})


class PostDetailView(DetailView):
    model = Post
    template_name = "post_detail.html"
    context_object_name = "post"



