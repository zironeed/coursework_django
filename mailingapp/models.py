from django.db import models
import datetime
NULLABLE = {'null': True, 'blank': True}


class Client(models.Model):
    email = models.EmailField(max_length=150, verbose_name='Почта')
    full_name = models.CharField(max_length=250, verbose_name='ФИО')
    comment = models.TextField(verbose_name='Комментарий', **NULLABLE)

    def __str__(self):
        return self.full_name

    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'


class MailingSettings(models.Model):

    class MailingSettingsStatus(models.TextChoices):
        Finished = 'Завершено'
        Created = 'Создано'
        Running = 'Выполнение'

    class MailingSettingsFrequency(models.TextChoices):
        Daily = 'День'
        Weekly = 'Неделя'
        Monthly = 'Месяц'

    title = models.CharField(max_length=100, verbose_name='Имя рассылки')
    time = models.DateTimeField(default=datetime.datetime(2023, 1, 1), verbose_name='Время рассылки')
    frequency = models.CharField(choices=MailingSettingsFrequency.choices, verbose_name='Частота рассылки')
    status = models.CharField(choices=MailingSettingsStatus.choices, verbose_name='Статус рассылки',
                              default=MailingSettingsStatus.Created)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Рассылка'
        verbose_name_plural = 'Рассылки'


class Message(models.Model):
    title = models.CharField(max_length=100, verbose_name='Тема письма')
    body = models.TextField(verbose_name='Тело письма')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Письмо'
        verbose_name_plural = 'Письма'


class Statistic(models.Model):

    class StatisticStatus(models.TextChoices):
        Finished = 'Выполнено'
        Created = 'Создано'

    last_try = models.DateTimeField(verbose_name='Последняя попытка', **NULLABLE)
    status = models.CharField(choices=StatisticStatus.choices, verbose_name='Статус попытки',
                              default=StatisticStatus.Created)
    answer = models.CharField(verbose_name='Ответ сервера', **NULLABLE)

    def __str__(self):
        return f'Последняя попытка: {self.last_try}, {self.status}. Ответ сервера: {self.answer}'

    class Meta:
        verbose_name = 'Лог'
        verbose_name_plural = 'Логи'
