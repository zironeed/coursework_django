from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
# Переменная для полей с нулевым значением
NULLABLE = {'blank': True, 'null': True}


class User(AbstractUser):
    '''Создаем пользователя через абстрактного пользователя, с полями полного имени, емейлом, комментарием и булево поле активный пользователь
    переписывает мод себя модель абстрактного пользователя убирая юзернейм и проставляя вместо него емейл'''

    username = None

    full_name = models.CharField(max_length=255, verbose_name='ФИО', **NULLABLE)
    email = models.EmailField(max_length=254, unique=True, verbose_name='контактный email')
    comment = models.CharField(max_length=255, verbose_name='комментарий', **NULLABLE)
    is_active = models.BooleanField(default=False, verbose_name='активный')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return f'{self.email}'

    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'

    def delete(self, *args, **kwargs):
        self.is_active = False
        self.save()

    class StatusType(models.Model):
        '''Класс для определения роли пользователя'''
        MANAGER = "MANAGER"
        BASE_USER = "BASE_USER"
        CONTENT_MANAGER = "CONTENT_MANAGER"
        STATUS = [
            (MANAGER, "Manager"),
            (BASE_USER, "Base_user"),
            (CONTENT_MANAGER, "Content_manager"),
        ]

    status_type = models.CharField(
        max_length=50,
        choices=StatusType.STATUS,
        default=StatusType.BASE_USER,
        verbose_name="роль")


class MailingClient(models.Model):
    '''Модель для клиента, которому будем отсылать письмо'''
    full_name = models.CharField(max_length=255, verbose_name='ФИО')
    contact_email = models.EmailField(max_length=254, unique=True, verbose_name='контактный email')
    comment = models.CharField(max_length=255, verbose_name='комментарий', **NULLABLE)

    class Meta:
        verbose_name = 'Клиент для рассылки'
        verbose_name_plural = 'Клиенты для рассылки'

    def __str__(self):
        return f'{self.contact_email}'
