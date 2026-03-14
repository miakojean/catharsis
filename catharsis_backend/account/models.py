from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser

# Create your models here.

class Customer(AbstractBaseUser):
    email = models.EmailField()
    phone_number = models.CharField(max_length=14) 
