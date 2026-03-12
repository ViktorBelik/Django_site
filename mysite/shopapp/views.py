"""
В этом модуле лежат различные наборы представлений.

Разные view интернет-магазина по:  товарам, заказам и т.д.
"""

import logging
from csv import DictWriter
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.core.cache import cache
from django.views import View
from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    PermissionRequiredMixin,
    UserPassesTestMixin
)
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)
from django.http import (
    HttpRequest,
    HttpResponse,
    HttpResponseRedirect,
    JsonResponse
)
from rest_framework.parsers import MultiPartParser
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.decorators import action
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema, OpenApiResponse
from yaml import serializer
from .models import Product, Order, ProductImage
from .forms import OrderForm, ProductForm
from .serializers import ProductSerializer
from .common import save_csv_products


log = logging.getLogger(__name__)


@extend_schema(description="Product views CRUD")
class ProductViewSet(ModelViewSet):
    """
    Набор представлений для действий над Product.

    Полный CRUD для сущностей товара.
    """

    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [
        SearchFilter,
        DjangoFilterBackend,
        OrderingFilter,
    ]
    search_fields = [
        "name",
        "description",
    ]
    filterset_fields = [
        "name",
        "description",
        "price",
        "discount",
        "archived",
    ]
    ordering_fields = [
        "name",
        "price",
        "discount",
    ]

    @extend_schema(
        summary="Get one product by ID",
        description="Retrieves **product**, returns 404 if not found",
        responses={
            200: ProductSerializer,
            404: OpenApiResponse(description="Empty response, product by id not found"),
        }
    )
    
    # Кэширование в REST Framework
    @method_decorator(cache_page(60 * 2))
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


    def retrieve(self, *args, **kwargs):
        return super().retrieve(*args, **kwargs)
    
    # Функция для преобразования JSON в CSV и скачивания файла обычными пользователями 
    @action(methods=["get"], detail=False)
    def download_csv(self, request: Request):
        response = HttpResponse(content_type="text/csv")
        filename = "products-export.csv"
        response["Content-Disposition"] = f"attachment; filename={filename}"
        queryset = self.filter_queryset(self.get_queryset())
        fields = [
            "name",
            "description",
            "price",
            "discount",
        ]
        queryset = queryset.only(*fields)
        writer = DictWriter(response, fieldnames=fields)
        writer.writeheader()
        
        for product in queryset:
            writer.writerow({
                field: getattr(product, field)
                for field in fields
            })
            
        return response
    
    # Функция для загрузки файла(Не работает, так как через терминал не передается объект User )
    # @action(methods=["post"], detail=False, parser_classes=[MultiPartParser])
    # def upload_csv(self, request: Request):
    #     products = save_csv_products(
    #         request,
    #         file=request.FILES["file"].file,
    #         encoding=request.encoding,
    #     )
    #     serializer = self.get_serializer(products, many=True)
    #     return Response(serializer.data)


class MainView(View):
    
    # @method_decorator(cache_page(60 * 2))
    def get(self, request: HttpRequest) -> HttpResponse:
        products = Product.objects.prefetch_related('images')
        context = {
            'products': products
        }
        # log.debug('Products for shop main: %s', products)
        # log.info('Rendering shop main')
        return render(request, 'shopapp/main.html', context=context)


class ProductDetailsView(DetailView):
    template_name = 'shopapp/product_details.html'
    queryset = Product.objects.prefetch_related('images')
    context_object_name = 'product'


class ProductsListView(ListView):
    template_name = 'shopapp/products_list.html'
    context_object_name = 'products'
    queryset = Product.objects.filter(archived=False)


class ProductCreateView(UserPassesTestMixin, CreateView):
    def test_func(self):
        my_user = self.request.user
        return my_user.groups.filter(name='secret-group').exists()
        # return my_user.is_superuser

    model = Product
    # fields = 'name', 'price', 'description', 'discount', 'preview'
    form_class = ProductForm
    template_name_suffix = '_create'
    success_url = reverse_lazy('shopapp:products_list')

    def form_valid(self, form):
        # Установление значения для поля created_by
        form.instance.created_by = self.request.user
        # Обработка загрузки нескольких картинок
        for image in form.files.getlist("images"):
            ProductImage.objects.create(
                product=self.object,
                image=image,
            )

        return super().form_valid(form)


class ProductUpdateView(UserPassesTestMixin, UpdateView):
    def test_func(self):
        my_user = self.request.user
        if my_user.is_superuser:
            return True
        elif (
            my_user == self.get_object().created_by and
            my_user.has_perm('shopapp.change_product')
        ):
            return True
        return False

    model = Product
    # fields = 'name', 'price', 'description', 'discount', 'preview'
    form_class = ProductForm
    template_name_suffix = '_update'

    def form_valid(self, form):
        # Обработка загрузки нескольких картинок
        for image in form.files.getlist("images"):
            ProductImage.objects.create(
                product=self.object,
                image=image,
            )

        return super().form_valid(form)

    def get_success_url(self) -> str:
        return reverse(
            'shopapp:product_details',
            kwargs={'pk': self.object.pk}
        )


class ProductArchiveView(UserPassesTestMixin, DeleteView):
    # Только администраторы
    def test_func(self):
        my_user = self.request.user
        if my_user.is_staff:
            return True
        return False

    template_name_suffix = '_confirm_archive'
    model = Product
    success_url = reverse_lazy('shopapp:products_list')

    # Замена удаления на архивирование
    def form_valid(self, form):
        success_url = self.get_success_url()
        self.object.archived = True
        self.object.save()
        return HttpResponseRedirect(success_url)


class ProductsDataExportView(View):
    def get(self, request: HttpRequest) -> JsonResponse:
        cache_key = "products_data_export"
        products_data = cache.get(cache_key)
        if products_data is None:
            products = Product.objects.order_by('pk').all()
            products_data = [
                {
                    "pk": product.pk,
                    "name": product.name,
                    "price": product.price,
                    "archived": product.archived,
                }
                for product in products
            ]
        cache.set(cache_key, products_data, 300)
        return JsonResponse({"products": products_data})


class OrderListView(LoginRequiredMixin, ListView):
    # queryset = (
    #     Order.objects
    #     .select_related('user')
    #     .prefetch_related('products')
    # )
    def get(self, request: HttpRequest) -> HttpResponse:
        my_user = self.request.user
        orders = my_user.orders.prefetch_related('products').all()
        context = {
            'orders': orders
        }
        return render(request, 'shopapp/order_list.html', context=context)


class OrderDetailView(PermissionRequiredMixin, DetailView):
    permission_required = 'shopapp.view_order'
    queryset = (
        Order.objects
        .select_related('user')
        .prefetch_related('products')
    )


class OrderCreateView(LoginRequiredMixin, CreateView):
    model = Order
    form_class = OrderForm
    template_name_suffix = '_create'
    success_url = reverse_lazy('shopapp:orders_list')

    def form_valid(self, form):
        # Установление значения для поля user
        form.instance.user = self.request.user

        return super().form_valid(form)


class OrderUpdateView(UpdateView):
    model = Order
    form_class = OrderForm
    template_name = 'shopapp/order_update.html'

    def get_success_url(self) -> str:
        return reverse(
            'shopapp:order_details',
            kwargs={'pk': self.object.pk}
        )


class OrderCancelView(UserPassesTestMixin, DeleteView):
    # Только администраторы и владелец
    def test_func(self):
        my_user = self.request.user
        if my_user.is_staff:
            return True
        elif self.get_object() == my_user:
            return True
        return False

    model = Order
    template_name_suffix = '_confirm_cancel'
    success_url = reverse_lazy('shopapp:orders_list')


class OrdersDataExportView(UserPassesTestMixin, View):
    def test_func(self):
        if self.request.user.is_staff:
            return True
        return False

    def get(self, request: HttpRequest) -> JsonResponse:
        orders = Order.objects.select_related('user').prefetch_related('products').order_by('pk').all()
        orders_data = [
            {
                "Order ID": order.pk,
                "Delivery address": order.delivery_address,
                "Promocode": order.promocode,
                "User ID": order.user.pk,
                "Products ID": [product.id for product in order.products.all()],
            }
            for order in orders
        ]
        return JsonResponse({"orders": orders_data})
