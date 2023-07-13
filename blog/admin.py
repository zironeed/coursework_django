from django.contrib import admin
from blog.models import Blog


@admin.register(Blog)
class ClientAdmin(admin.ModelAdmin):
    list_display = ("title", "date", "views")
    search_fields = ("title",)
    list_filter = ("title", "date")
