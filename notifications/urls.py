from django.urls import path
from .views import *

app_name = 'notifications'

urlpatterns = [
    path('notifications', NotificationsListView.as_view(), name='notifications'),
    path('delete-notification/<int:id>', delete_notification, name='delete-notification')

]