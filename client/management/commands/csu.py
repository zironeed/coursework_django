from django.core.management import BaseCommand

from client.models import User


class Command(BaseCommand):
    '''Команда для создания админа'''

    def handle(self, *args, **options):
        user = User.objects.create(
            email="admin@admin.ru",
            first_name="Admin",
            last_name="Admin",
            is_staff=True,
            is_superuser=True,
            is_active=True
        )

        user.set_password('12345')
        user.save()
