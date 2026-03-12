from typing import Any, Sequence
from django.contrib.auth import get_user_model
from django.core.management import BaseCommand
from shopapp.models import Product


class Command(BaseCommand):
    def handle(self, *args: Any, **options: Any):
        self.stdout.write('Start demo select fields')
         
        users_info = get_user_model().objects.values_list("pk", "username")
        for user_info in users_info:
            print(user_info)

        # products_values = Product.objects.values("pk", "name")
        # for p_values in products_values:
        #     print(p_values)

        self.stdout.write('Done')
