from django import forms

from client.models import MailingClient
from mailing import models


class StyleFormMixin:
    '''Форма для выравнивания непосредственно самих форм в html'''

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


class MailForm(StyleFormMixin, forms.ModelForm):
    '''Форма для письма с переменной которая выводит в список и дает выбрать нескольких клиентов'''
    clients = MailingClient.objects.all()
    client_to_message = forms.ModelMultipleChoiceField(queryset=clients, required=False)

    class Meta:
        model = models.Mail
        fields = ('mailing_subject', 'mailing_body', 'client_to_message', 'all_clients',)


class SettingsForm(StyleFormMixin, forms.ModelForm):
    '''Форма для настроек рассылки'''

    class Meta:
        model = models.MailingSettings
        fields = ('mailing_time_start', 'mailing_time_end', 'mailing_periods',)
        widgets = {
            'mailing_time_start': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'mailing_time_end': forms.DateTimeInput(attrs={'type': 'datetime-local'})
        }


class MailingClientForm(StyleFormMixin, forms.ModelForm):
    '''Форма для получателей рассылки'''

    class Meta:
        model = models.MailingClient
        fields = ('full_name', 'contact_email', 'comment',)
