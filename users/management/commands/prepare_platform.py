from django.core.management import BaseCommand
from users.models import Users
from django.contrib.auth.models import Group
from django.contrib.auth.models import Permission
import psycopg2
import os


def send_query(table, args):
    connection = psycopg2.connect(
        host='localhost',
        database=os.getenv('BASE_NAME'),
        user=os.getenv('BASE_USER'),
        password=os.getenv('BASE_PASSWORD')
        )

    try:
        with connection:
            with connection.cursor() as cursor:
                query = f"INSERT INTO {table} VALUES {args}"
                cursor.execute(query)
                connection.commit()
                print("Set user roles")
    except psycopg2.Error:
        print("Set user roles. Error!")
    finally:
        connection.close()


class Command(BaseCommand):

    def handle(self, *args, **options):

        # create moderators group
        GROUPS = ['moderators', ]
        MODELS = ["Client", "Message", "Transmission", "user", ]
        PERMISSIONS = ['view', ]

        for group in GROUPS:
            new_group, created = Group.objects.get_or_create(name=group)
            for model in MODELS:
                for permission in PERMISSIONS:
                    name = 'Can {} {}'.format(permission, model)
                    print("Creating {}".format(name))
                    model_add_perm = Permission.objects.get(name=name)
                    new_group.permissions.add(model_add_perm)

        # create users group
        GROUPS = ['users', ]
        MODELS = ["Client", "Message", "Transmission", ]
        PERMISSIONS = ["add", "change", "delete", "view", ]

        for group in GROUPS:
            new_group, created = Group.objects.get_or_create(name=group)
            for model in MODELS:
                for permission in PERMISSIONS:
                    name = 'Can {} {}'.format(permission, model)
                    print("Creating {}".format(name))
                    model_add_perm = Permission.objects.get(name=name)
                    new_group.permissions.add(model_add_perm)

        user = Users.objects.create(
            email="admin@gmail.com",
            first_name="admin",
            last_name="admin",
            is_superuser=True,
            is_staff=True,
            is_active=True
        )

        user.set_password("admin")
        user.save()
        print("Creating user admin.")

        user = Users.objects.create(
            email="moderator@gmail.com",
            first_name="moderator",
            last_name="moderator",
            is_superuser=False,
            is_staff=True,
            is_active=True
        )
        user.set_password("moderator")
        user.save()
        print("Creating user moderator.")

        user = Users.objects.create(
            email="test@gmail.com",
            first_name="test",
            last_name="test",
            is_superuser=False,
            is_staff=False,
            is_active=True
        )
        user.set_password("test")
        user.save()
        print("Creating user test.")

        send_query("users_user_groups", "('1', '2', '1')")
        send_query("users_user_groups", "('2', '3', '2')")
