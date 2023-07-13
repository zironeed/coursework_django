from django.db import models
from config import settings

import django as django
import datetime

NULLABLE = {'null': True, 'blank': True}


class Client(models.Model):
    email = models.EmailField(max_length=150, verbose_name='Почта')
    full_name = models.CharField(max_length=250, verbose_name='ФИО', unique=True)
    comment = models.TextField(verbose_name='Комментарий', **NULLABLE)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, verbose_name='Владелец')

    def __str__(self):
        return self.full_name

    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'


class MailingSettings(models.Model):

    class MailingSettingsStatus(models.TextChoices):
        Finished = 'FINISHED'
        Created = 'CREATED'
        Running = 'READY'
        Finished_error = 'FINISHED_WITH_ERROR'

    class MailingSettingsFrequency(models.TextChoices):
        Daily = 'DAILY'
        Weekly = 'WEEKLY'
        Monthly = 'MONTHLY'

    title = models.CharField(max_length=100, verbose_name='Имя рассылки', unique=True)
    time = models.TimeField(verbose_name="Начало рассылки", default=django.utils.timezone.now)
    frequency = models.CharField(choices=MailingSettingsFrequency.choices, verbose_name='Частота рассылки')
    status = models.CharField(choices=MailingSettingsStatus.choices, verbose_name='Статус рассылки',
                              default=MailingSettingsStatus.Created)
    message = models.ForeignKey('Message', on_delete=models.SET_NULL, **NULLABLE, verbose_name='Письмо')
    client = models.ManyToManyField('Client', verbose_name='Клиент')
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, verbose_name='Владелец')
    is_published = models.BooleanField(default=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Рассылка'
        verbose_name_plural = 'Рассылки'

    def get_statistic(self):
        return self.statistic_of_mailing.all()

    def get_messages(self):
        messages = self.message
        return messages

    def get_clients(self):
        clients = self.client.all()
        return clients


class Message(models.Model):
    title = models.CharField(max_length=100, verbose_name='Тема письма', unique=True)
    body = models.TextField(verbose_name='Тело письма')
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, verbose_name='Владелец')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Письмо'
        verbose_name_plural = 'Письма'

    def get_info(self):
        return self.title, self.body


class Statistic(models.Model):

    class StatisticStatus(models.TextChoices):
        Finished = 'FINISHED'
        Created = 'CREATED'

    mailing = models.ForeignKey("MailingSettings", on_delete=models.CASCADE, related_name="statistic_of_mailing",
                                verbose_name='Рассылка', **NULLABLE)
    time = models.DateTimeField(verbose_name='Последняя попытка', **NULLABLE)
    status = models.CharField(choices=StatisticStatus.choices, verbose_name='Статус попытки',
                              default=StatisticStatus.Created)
    mail_answer = models.CharField(verbose_name='Ответ сервера', **NULLABLE, default=None)

    def __str__(self):
        return f'Последняя попытка: {self.time}, {self.status}. Ответ сервера: {self.mail_answer}'

    class Meta:
        verbose_name = 'Лог'
        verbose_name_plural = 'Логи'
