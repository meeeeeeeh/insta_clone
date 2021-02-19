from django.shortcuts import render
from .models import *
from django.views.generic import ListView


class HomeView(ListView):
    model = Post
    template_name = 'index.html'
    context_object_name = 'posts'