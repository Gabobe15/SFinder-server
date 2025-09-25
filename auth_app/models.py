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
    ('student', 'Student'),
    ('admin', 'Admin'),
    ('university', 'University'),
)
    
class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(max_length=200, unique=True)
    fullname = models.CharField(max_length=200)
    role = models.CharField(max_length=20, default='student', choices=ROLE_CHOICE)
    mobile = models.CharField(max_length=200, blank=True, null=True)
    sex = models.CharField(max_length=20, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    
    is_active = models.BooleanField(default=True)

    category = models.ForeignKey("core.Category", on_delete=models.SET_NULL, null=True, blank=True, related_name="users")


    # created_at = models.DateTimeField(auto_now_add=True)

    
    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['fullname', 'role']
    
    def __str__(self):
        return self.email