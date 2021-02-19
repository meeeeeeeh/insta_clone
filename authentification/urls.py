from django.urls import path
from .views import *
from django.contrib.auth import views as authViews

app_name = 'authentification'

urlpatterns = [
    path('signup/', SignUp, name='signup'),
    path('login/', authViews.LoginView.as_view(template_name='login.html'), name='login')
]