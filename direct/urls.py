from django.urls import path
from .views import *


app_name = 'direct'

urlpatterns = [
    path('chat/<slug:username>', direct_with_user, name="direct-with-user"),
    path('directs', DirectView.as_view(), name="directs"),
    path('create_direct/<int:user_id>', create_direct, name='create-direct')
]