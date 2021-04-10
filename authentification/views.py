from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.urls import reverse_lazy

from .forms import SignupForm, ChangePasswordForm, EditProfileForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from django.views.generic import TemplateView, UpdateView, ListView
from post.models import Post, Likes, Follow
from django.shortcuts import get_object_or_404
from .models import Profile


def sign_up(request):
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
def password_change(request):
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


def password_change_done(request):
    return render(request, 'change_password_done.html')


class UserProfile(TemplateView):
    template_name = "profile.html"

    def get_context_data(self, **kwargs):
        context = super(UserProfile, self).get_context_data(**kwargs)
        user = get_object_or_404(User, username=kwargs["username"])
        context['user'] = user
        context['profile'] = Profile.objects.get(user=user)
        context['follow_status'] = Follow.objects.filter(following=user, follower=self.request.user).exists()
        context['following_count'] = Follow.objects.filter(follower=user).count()
        context['followers_count'] = Follow.objects.filter(following=user).count()
        context['posts'] = Post.objects.filter(user=user).order_by('-posted')

        return context


class EditProfile(UpdateView):
    template_name = "edit_profile.html"
    model = Profile
    form_class = EditProfileForm

    def get_success_url(self, **kwargs):
        return reverse_lazy('authentification:profile', kwargs={'username': self.request.user.username})


class UserFollowers(TemplateView):
    template_name = 'user_followers.html'

    def get_context_data(self, **kwargs):
        context = super(UserFollowers, self).get_context_data(**kwargs)
        user = get_object_or_404(User, username=kwargs["username"])
        context['followers'] = Follow.objects.filter(following=user)
        return context


class UserFollowing(TemplateView):
    template_name = 'user_following.html'

    def get_context_data(self, **kwargs):
        context = super(UserFollowing, self).get_context_data(**kwargs)
        user = get_object_or_404(User, username=kwargs["username"])
        context['followings'] = Follow.objects.filter(follower=user)
        return context
