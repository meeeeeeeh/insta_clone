from django.urls import path
from .views import *

app_name = 'post'

urlpatterns = [
    path('', HomeView.as_view(), name='index')
]