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
    time = models.TimeField(verbose_name="Начало рассылки", default=datetime.datetime.now().time())
    frequency = models.CharField(choices=MailingSettingsFrequency.choices, verbose_name='Частота рассылки')
    status = models.CharField(choices=MailingSettingsStatus.choices, verbose_name='Статус рассылки',
                              default=MailingSettingsStatus.Created)
    message = models.ForeignKey('Message', on_delete=models.SET_NULL, **NULLABLE, verbose_name='Письмо')
    client = models.ManyToManyField('Client', verbose_name='Клиент')
    statistic = models.OneToOneField('Statistic', on_delete=models.CASCADE, **NULLABLE, default=None,
                                     verbose_name='Статистика')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Рассылка'
        verbose_name_plural = 'Рассылки'

    @property
    def get_statistic(self):
        return self.statistic_of_mailing.all()


class Message(models.Model):
    title = models.CharField(max_length=100, verbose_name='Тема письма')
    body = models.TextField(verbose_name='Тело письма')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Письмо'
        verbose_name_plural = 'Письма'

    def get_info(self):
        return self.title, self.body


class Statistic(models.Model):

    class StatisticStatus(models.TextChoices):
        Finished = 'Выполнено'
        Created = 'Создано'

    mailing = models.ForeignKey("MailingSettings", on_delete=models.CASCADE, related_name="statistic_of_mailing",
                                verbose_name='Рассылка', **NULLABLE)
    last_try = models.DateTimeField(verbose_name='Последняя попытка', **NULLABLE)
    status = models.CharField(choices=StatisticStatus.choices, verbose_name='Статус попытки',
                              default=StatisticStatus.Created)
    answer = models.CharField(verbose_name='Ответ сервера', **NULLABLE)

    def __str__(self):
        return f'Последняя попытка: {self.last_try}, {self.status}. Ответ сервера: {self.answer}'

    class Meta:
        verbose_name = 'Лог'
        verbose_name_plural = 'Логи'
