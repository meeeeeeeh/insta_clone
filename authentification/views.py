from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .forms import SignupForm, ChangePasswordForm, EditProfileForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from django.views.generic import TemplateView
from post.models import Post, Likes
from django.shortcuts import get_object_or_404


def SignUp(request):
    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            User.objects.create_user(username=username, email=email, password=password)
            return redirect('authentification:login')
    else:
        form = SignupForm()
    context = {'form': form, }

    return render(request, 'signup.html', context)


@login_required
def PasswordChange(request):
    user = request.user
    if request.method == "POST":
        form = ChangePasswordForm(request.POST)
        if form.is_valid():
            new_password = form.cleaned_data.get('new_password')
            user.set_password(new_password)
            user.save()
            update_session_auth_hash(request, user)
            return redirect('authentification:change_password_done')
    else:
        form = ChangePasswordForm(instance=user)
    context = {'form': form}

    return render(request, 'change_password.html', context)


def PasswordChangeDone(request):
    return render(request, 'change_password_done.html')


class UserProfile(TemplateView):
    template_name = "profile.html"

    def get_context_data(self, **kwargs):
        context = super(UserProfile, self).get_context_data(**kwargs)
        user = get_object_or_404(User, username=kwargs["username"])
        context['posts'] = Post.objects.filter(user=user).order_by('-posted')
        context['user'] = user
        return context