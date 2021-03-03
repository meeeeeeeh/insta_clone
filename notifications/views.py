from django.shortcuts import render, redirect
from django.views.generic import ListView
from .models import Notification


class NotificationsListView(ListView):
    template_name = 'notifications.html'
    model = Notification
    context_object_name = 'notifications'

    def get_queryset(self):
        notifications = Notification.objects.filter(user=self.request.user).order_by('-date')
        Notification.objects.filter(user=self.request.user, is_seen=False).update(is_seen=True)
        return notifications


def delete_notification(request, id):
    user = request.user
    Notification.objects.filter(id=id, user=user).delete()
    return redirect('notifications:notifications')


def notifications_count(request):
    noti_count = 0
    if request.user.is_authenticated:
        noti_count = Notification.objects.filter(user=request.user, is_seen=False).count()

    return {'noti_count': noti_count}
