from django.urls import path
from .views import *

app_name = 'post'

urlpatterns = [
    path('', HomeView.as_view(), name='index'),
    path('post/<uuid:pk>', PostDetailView, name='post_detail'),
    path('post/like/<uuid:pk>', like, name='post_like'),
    path('post/new', create_post, name="post_create"),
]