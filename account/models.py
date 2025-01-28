from django.contrib.auth.models import AbstractUser, BaseUserManager, UserManager
from django.db import models

from account.managers import CustomUserManager, CustomBaseUserManager



class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(unique=True)
    
    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    
    

