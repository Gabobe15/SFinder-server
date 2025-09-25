from django.urls import path, include
from .views import *






urlpatterns = [
    path('register', RegisterView.as_view(), name='register'),
    path('login', LoginView.as_view(), name='login'),
    path('change-password', ChangePasswordView.as_view(), name='change password'),
    path('logout', LogoutView.as_view(), name='logout'),
    
    # forget
    path('forget-password', PasswordResetRequestView.as_view(), name='forget-password'),
    
    # reset 
    path('reset-password', PasswordResetConfirmView.as_view(), name='reset-password'),
    
    
    
    path('user/', UserView.as_view(), name='user'),
    path('users', UsersList.as_view(), name='users'),
    path('university-list', UniversityList.as_view(), name='university-list'),
    path('users/<int:id>/activate/', UserActivationView.as_view(), name="user-activate"),
]

