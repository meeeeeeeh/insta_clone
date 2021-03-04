from django.urls import path
from .views import *

app_name = 'stories'

urlpatterns = [
    path('new_story', new_story, name='new_story'),
    path('show_story/<stream_id>', show_story, name='show_story')
]