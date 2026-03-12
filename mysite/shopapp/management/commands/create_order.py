from typing import Any, Sequence
from django.core.management import BaseCommand
from django.contrib.auth import get_user_model
from django.db import transaction
from shopapp.models import Order, Product


class Command(BaseCommand):
    @transaction.atomic
    def handle(self, *args: Any, **options: Any):
        self.stdout.write('Create order with products')
        user = get_user_model().objects.get(username='Admin')
        # products: Sequence[Product] = Product.objects.all()
        # products: Sequence[Product] = Product.objects.defer('description', 'price', 'created_at').all()
        products: Sequence[Product] = Product.objects.only('id').all()
        order, created = Order.objects.get_or_create(
            delivery_address='Ivanova street, d 11',
            promocode='promo5',
            user=user,
        )
        for product in products:
            order.products.add(product)
        order.save()
        self.stdout.write(f'Create order {order}')
