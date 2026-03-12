from .models import Product


from django.db import connection


from csv import DictReader
from io import TextIOWrapper


def save_csv_products(request, file, encoding):
    csv_file = TextIOWrapper(file, encoding)
    reader = DictReader(csv_file)
    products = [
        Product(created_by=request.user, **row)
        for row in reader
    ]
    # Запрос к базе данных для корректной работы bulk_create
    connection.ensure_connection()

    Product.objects.bulk_create(products)

    return products