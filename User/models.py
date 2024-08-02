from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
class User(AbstractUser):
    MY_ROLES =[
        ('Admin','Admin'),
        ('Staff','Staff'),
        ('Unknown','Unknown')
    ]
    role = models.CharField(max_length=50, choices=MY_ROLES)

