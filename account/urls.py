from django.urls import path
from django.contrib.auth import views as auth_views

from account import views

app_name = 'account'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('register/', views.UserRegistrationView.as_view(), name='register'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/',
         auth_views.LogoutView.as_view(
             template_name='registration/logout.html'),
         name='logout'),
]
