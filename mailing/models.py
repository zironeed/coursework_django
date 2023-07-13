from django.db import models

from django.urls import reverse_lazy
from pytils.translit import slugify

from client.models import NULLABLE, MailingClient
from config.settings import AUTH_USER_MODEL


class Status(models.TextChoices):
    '''Варианты для выбора статуса рассылки'''
    ACTIVE = 'AC', 'Active'
    FINISHED = 'FI', 'Finished'
    CREATED = 'CR', 'Created'


class Periods(models.TextChoices):
    '''Варианты для выбора периодичности рассылки'''
    DAILY = 'DL', 'Daily'
    WEEKLY = 'WL', 'Weekly'
    MONTHLY = 'ML', 'Monthly'


class MailingSettings(models.Model):
    '''Модель настроек рассылки с полями статуса, времени начала и конца, периода рассылки и автора'''
    mailing_status = models.CharField(max_length=2, choices=Status.choices, default=Status.CREATED,
                                      verbose_name='статус рассылки')
    mailing_time_start = models.DateTimeField(verbose_name='время начала рассылки', **NULLABLE)
    mailing_time_end = models.DateTimeField(verbose_name='время конца рассылки', **NULLABLE)
    mailing_periods = models.CharField(max_length=2, choices=Periods.choices, verbose_name='периодичность')
    author = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE, **NULLABLE)

    def __str__(self):
        return f'{self.mailing_status}({self.mailing_time_start}), {self.mailing_periods}'

    class Meta:
        verbose_name = 'Настройка рассылки'
        verbose_name_plural = 'Настройки рассылки'
        ordering = ["mailing_status"]


class Mail(models.Model):
    '''Модель письма рассылки с полями настроек, получателя, темы письма, тела письма, выбора всех клиентов и булевым полем активности'''
    client_to_message = models.ManyToManyField(MailingClient, verbose_name='Клиенты', **NULLABLE, related_name='client_to_message')
    settings = models.ForeignKey(MailingSettings, on_delete=models.CASCADE)
    mailing_subject = models.CharField(max_length=255, verbose_name='тема письма')
    mailing_body = models.CharField(max_length=500, verbose_name='тело письма')
    all_clients = models.BooleanField(verbose_name='все клиенты', **NULLABLE)

    is_active = models.BooleanField(default=True, verbose_name='активный')

    def __str__(self):
        return f'{self.mailing_subject}: {self.mailing_body}'

    class Meta:
        verbose_name = 'Письмо'
        verbose_name_plural = 'Письма'




class MailingTry(models.Model):
    '''Модель попытки рассылки с полями настроек, даты и времени последней рассылки, статусом рассылки и ответом почтового сервера'''
    mailing = models.ForeignKey(MailingSettings, on_delete=models.CASCADE)
    mailing_try = models.DateTimeField(auto_now=True, verbose_name='дата и время последней попытки')
    mailing_try_status = models.CharField(max_length=255, verbose_name='статус рассылки', **NULLABLE)
    mailing_response = models.CharField(max_length=255, verbose_name='ответ почтового сервера', **NULLABLE)

    def __str__(self):
        return f'{self.mailing_try.strftime("%d.%m.%Y %H:%M")} ({self.mailing_try_status}): {self.mailing_response}'

    class Meta:
        verbose_name = 'Попытка рассылки'
        verbose_name_plural = 'Попытки рассылки'


class Blog(models.Model):
    '''Модель блога, включает в себя заголовок, slug слово для урлов, содержимое, картинку, дату создания и просмотры'''
    name = models.CharField(max_length=100, verbose_name='заголовок')
    slug = models.CharField(max_length=100, verbose_name='slug')
    post = models.CharField(max_length=100, verbose_name='содержимое')
    image = models.ImageField(upload_to='img/', verbose_name='изображение', **NULLABLE)
    creation_date = models.DateTimeField(auto_now_add=True, verbose_name='дата создания')
    total_views = models.IntegerField(default=0, verbose_name='просмотры')

    def __str__(self):
        return f'{self.name} {self.slug} {self.post} {self.creation_date}  {self.total_views}'

    def save(self, *args, **kwargs):
        '''функция для сохранения slug'''
        self.slug = slugify(str(self.name)) + str(self.id)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        '''функция для получения абсолютного адреса со slug'''
        return reverse_lazy('mailing:blog_details', kwargs={'slug': self.slug})

    class Meta:
        verbose_name = 'блог'
        verbose_name_plural = 'блоги'
