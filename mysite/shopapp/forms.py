from django import forms
from django.forms import ModelForm
from .models import Product, Order


class ProductForm(ModelForm):
    class Meta:
        model = Product
        fields = 'name', 'price', 'description', 'discount', 'preview'

    # required=False позволяет полю оставаться пустым
    images = forms.ImageField(required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Добавление атрибута "multiple" для возможности выбора нескольких файлов
        self.fields["images"].widget.attrs.update({"multiple": "true"})


class OrderForm(ModelForm):
    class Meta:
        model = Order
        fields = 'delivery_address', 'promocode', 'products'


class CSVImportForm(forms.Form):
    csv_file = forms.FileField()