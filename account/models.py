from django.db import models

from django.contrib.auth.models import User

class AbstractBaseUser(models.Model):
    username = models.CharField()
