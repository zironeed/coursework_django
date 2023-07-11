from django.contrib import admin
from mailingapp.models import Client, MailingSettings, Message, Statistic


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ("full_name", "email", "comment")
    search_fields = ("full_name", "email")
    list_filter = ("full_name", "email")


@admin.register(MailingSettings)
class TransmissionAdmin(admin.ModelAdmin):
    list_display = ("title", "time", "frequency", "status", "statistic")
    list_filter = ("status",)
    filter_horizontal = ["clients"]


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ("theme",)
    search_fields = ("theme",)
    list_filter = ("theme",)


@admin.register(Statistic)
class AttemptAdmin(admin.ModelAdmin):
   list_display = ("time", "status", "mail_answer",)
