from django.shortcuts import render, redirect
from .models import *
from django.views.generic import TemplateView
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.utils.safestring import mark_safe
import json
from .models import Message


class DirectView(TemplateView):
    template_name = 'direct.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['directs'] = Room.objects.filter(Q(sender=self.request.user) | Q(receiver=self.request.user))
        return context


@login_required
def create_direct(request, user_id):
    user = User.objects.get(id=user_id)
    if not Room.objects.filter(Q(sender=request.user, receiver=user) | Q(sender=user, receiver=request.user)) \
            .exists():
        Room.objects.create(sender=request.user, receiver=user)

    return redirect('direct:directs')


@login_required
def direct_with_user(request, username):
    directs = Room.objects.filter(Q(sender=request.user) | Q(receiver=request.user))
    user = User.objects.get(username=username)
    messages = Message.objects.filter(sender=user, receiver=request.user, is_read=False)
    messages.update(is_read=True)

    return render(request, 'direct.html', {
        'directs': directs,
        'user_json': mark_safe(json.dumps(username)),
        'username': mark_safe(json.dumps(request.user.username))
    })


def check_directs(request):
    directs_count = 0
    if request.user.is_authenticated:
        directs_count = Message.objects.filter(receiver=request.user, is_read=False).count()
    return {'directs_count': directs_count}
