from django.urls import path, include
from .views import *






urlpatterns = [
    path('auth/register', RegisterView.as_view(), name='register'),
    path('auth/login', LoginView.as_view(), name='login'),
    path('auth/change-password', ChangePasswordView.as_view(), name='change password'),
    path('auth/logout', LogoutView.as_view(), name='logout'),
    
    # forget
    path('auth/forget-password', PasswordResetRequestView.as_view(), name='forget-password'),
    
    # reset 
    path('auth/reset-password', PasswordResetConfirmView.as_view(), name='reset-password'),
    
    
    
    path('user', UserView.as_view(), name='user'),
    path('users', UsersList.as_view(), name='users'),
]

