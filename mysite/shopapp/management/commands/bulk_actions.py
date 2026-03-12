from typing import Any, Sequence
from django.contrib.auth import get_user_model
from django.core.management import BaseCommand
from shopapp.models import Product
from django.db import connection


class Command(BaseCommand):
    def handle(self, *args: Any, **options: Any):
        self.stdout.write('Start demo bulk actions')

        # Массовое обновление продуктов
        result = Product.objects.filter(
            name__contains='Smartphone'
        ).update(discount=10)

        print(result)

        # Массовое создание продуктов
        # # Встроенный метод Django, который позволяет проверить соединение с базой данных без запроса данных
        # # connection.ensure_connection()

        # user = get_user_model().objects.filter(username='Admin')
        # info = [
        #     ('Smartphone 3', 23999, *user),
        #     ('Smartphone 4', 25000, *user),
        #     ('Smartphone 5', 20500, *user),
        # ]
        # products = [
        #     Product(name=name, price=price, created_by=created_by)
        #     for name, price, created_by in info
        # ]

        # result = Product.objects.bulk_create(products)
        # for obj in result:
        #     print(obj)

        self.stdout.write('Done')
