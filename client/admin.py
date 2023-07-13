from django.contrib import admin

from client.models import User, MailingClient

# Register your models here.

# Регистрируем в админке 2 модели
admin.site.register(User)

admin.site.register(MailingClient)
