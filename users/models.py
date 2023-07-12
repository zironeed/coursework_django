from django.db import models
from django.contrib.auth.models import AbstractUser
NULLABLE = {'null': True, 'blank': True}


class Users(AbstractUser):

    username = None

    email = models.EmailField(unique=True, verbose_name="Почта")
    phone = models.CharField(max_length=50, verbose_name="Телефон", **NULLABLE)
    country = models.CharField(max_length=50, verbose_name="Страна", **NULLABLE)
    avatar = models.ImageField(upload_to="Аватар", **NULLABLE)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
