from django.urls import path
from .views import *

app_name = "follow"

urlpatterns = [
    path('follow/<username>', follow_user, name="follow"),
    path('unfollow/<username>', unfollow_user, name="unfollow"),
]