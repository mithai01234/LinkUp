# In your models.py

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, Group, Permission
from django.db import models

class CustomUserManager(BaseUserManager):
    def create_user(self, email, phone_number, password=None, **extra_fields):
        if not email:
            raise ValueError('The email must be set')

        email = self.normalize_email(email)
        user = self.model(email=email, phone_number=phone_number, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, phone_number, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, phone_number, password, **extra_fields)

class CustomUser(AbstractBaseUser):
    id = models.AutoField(primary_key=True)
    email = models.EmailField(unique=True)
    otp = models.CharField(max_length=6, blank=True)
    phone_number = models.CharField(max_length=15)
    password = models.CharField(max_length=128)  # No need to store password directly
    status = models.BooleanField(default=False)
    name = models.CharField(max_length=50, blank=True)
    address = models.TextField(blank=True)
    gender=models.BooleanField(blank=True)
    profile_photo=models.ImageField(upload_to='images/', null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['phone_number']

    def __str__(self):
        return self.email

    class Meta:
        ordering = ['email']  # Adjust ordering field

# In your admin.py

from django.db import models


class Link(models.Model):
    id = models.IntegerField(primary_key=True)
    user_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    url = models.URLField()

    def __str__(self):
        return self.url

