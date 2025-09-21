from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True, verbose_name='E-mail')
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True, verbose_name='avatar')
    phone_number = models.CharField(max_length=15, blank=True, null=True, verbose_name='phone number')
    country = models.CharField(max_length=65, blank=True, null=True, verbose_name='country')

    USERNAME_FIELD = 'email'  # Для авторизации в качестве username будем использовать email
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email