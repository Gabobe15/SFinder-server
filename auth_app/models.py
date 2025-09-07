from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.base_user import BaseUserManager
from django.utils.timezone import now, timedelta
from django.db.models.signals import post_save


# Create your models here.
class CustomUserManager(BaseUserManager):
    def create_user(self,email,password=None, **extra_fields):
        if not email:
            raise ValueError('Email is required field')
        
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user 
    
    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email,password, **extra_fields)

ROLE_CHOICE = (
    ('user', 'User'),
    ('admin', 'Admin'),
    ('uni', 'University'),
)
    
class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(max_length=200, unique=True)
    fullname = models.CharField(max_length=200)
    role = models.CharField(max_length=20, default='user', choices=ROLE_CHOICE)
    tel_no = models.CharField(max_length=200)
    sex = models.CharField(max_length=10)
    
    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['fullname', 'role', 'tel_no', 'sex']
    
    def __str__(self):
        return self.email