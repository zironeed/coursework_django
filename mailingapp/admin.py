from django.contrib import admin
from mailingapp.models import Client, MailingSettings, Message, Statistic


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ("full_name", "email", "comment")
    search_fields = ("full_name", "email")
    list_filter = ("full_name", "email")


@admin.register(MailingSettings)
class MailingSettings(admin.ModelAdmin):
    list_display = ("title", "time", "frequency", "status", "is_published")
    list_filter = ("status",)
    filter_horizontal = ["client"]


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ("title",)
    search_fields = ("title",)
    list_filter = ("title",)


@admin.register(Statistic)
class AttemptAdmin(admin.ModelAdmin):
   list_display = ("time", "status", "mail_answer",)
