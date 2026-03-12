from django.db import models
from django.conf import settings
import shutil
import os


def product_preview_directory_path(instance: "Product", filename: str) -> str:
    path = "products/product_{pk}/preview".format(
        pk=instance.pk,
    )
    path_to_dir = os.path.join(settings.MEDIA_ROOT, path)
    if os.path.exists(path_to_dir):
        shutil.rmtree(path_to_dir)
    path_to_file = os.path.join(path, filename)
    return path_to_file


class Product(models.Model):
    """
    Модель Product представляет товар, который можно продавать в интернет-магазине.

    Заказы тут: :model:`shopapp.Order`
    """

    class Meta:
        # Этот параметр указывает, по каким полям модели будут сортироваться записи, возвращаемые при запросе.
        ordering = ['name', 'price']
        # db_table = 'tech_products'
        # verbose_name_plural = 'products'

    name = models.CharField(max_length=100, db_index=True)
    description = models.TextField(null=False, blank=True, db_index=True)
    price = models.DecimalField(default=0, max_digits=8, decimal_places=2)
    discount = models.PositiveSmallIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    archived = models.BooleanField(default=False)
    preview = models.ImageField(null=True, blank=True, upload_to=product_preview_directory_path)

    # @property
    # def description_short(self) -> str:
    #     if len(self.description) < 48:
    #         return self.description
    #     return self.description[:48] + '...'

    def __str__(self) -> str:
        return f'Product(pk={self.pk}, name={self.name!r})'


def product_images_directory_path(instance: "ProductImage", filename: str) -> str:
    path = "products/product_{pk}/images".format(
        pk=instance.product.pk,
    )
    path_to_dir = os.path.join(settings.MEDIA_ROOT, path)
    if os.path.exists(path_to_dir) and len(os.listdir(path_to_dir)) > 9:
        shutil.rmtree(path_to_dir)
        instance.delete(False)
    path_to_file = os.path.join(path, filename)
    return path_to_file


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(null=True, blank=True, upload_to=product_images_directory_path)
    description = models.CharField(max_length=200, null=False, blank=True)


def order_receipt_directory_path(instance: "Order", filename: str) -> str:
    return "users/user_{username}/orders/order_{pk}/receipt/{filename}".format(
        username=instance.user.username,
        pk=instance.pk,
        filename=filename,
    )


class Order(models.Model):
    delivery_address = models.TextField(null=True, blank=True)
    promocode = models.CharField(max_length=20, null=False, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='orders')
    products = models.ManyToManyField(Product, related_name='orders')
    receipt = models.FileField(null=True, upload_to=order_receipt_directory_path)
