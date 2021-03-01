from django.urls import path, reverse_lazy
from .views import *
from django.contrib.auth import views as authViews

app_name = 'authentification'

urlpatterns = [
    path('signup/', SignUp, name='signup'),
    path('login/', authViews.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', authViews.LogoutView.as_view(next_page=reverse_lazy('authentification:login')), name="logout"),
    path('change_password', PasswordChange, name='change_password'),
    path('change_password_done', PasswordChangeDone, name="change_password_done"),
    path('profile/<username>', UserProfile.as_view(), name="profile"),
    path('profile/edit_profile/<pk>', EditProfile.as_view(), name="edit_profile"),
]
