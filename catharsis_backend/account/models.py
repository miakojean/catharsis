from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils import timezone
import uuid
import re

class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("L'adresse email est obligatoire")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)

class Customer(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=14, blank=True, null=True)
    
    # Métriques et Statuts
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)

    # Identifiant de connexion
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = [] # L'email est déjà requis via USERNAME_FIELD

    objects = UserManager()

    def __str__(self):
        return self.email

    @property
    def initials(self):
        if not self.email:
            return "??"
        username_part = self.email.split('@')[0]
        parts = [p for p in re.split(r'[._\-+]+', username_part) if p]
        if len(parts) >= 2:
            return f"{parts[0][0]}{parts[1][0]}".upper()
        elif len(username_part) >= 2:
            return username_part[:2].upper()
        elif len(username_part) == 1:
            return username_part.upper()
        return "??"
