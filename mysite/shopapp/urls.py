from django.urls import path, include
from django.views.decorators.cache import cache_page
from rest_framework.routers import DefaultRouter
from .views import (
    MainView,
    ProductDetailsView,
    ProductsListView,
    OrderListView,
    OrderDetailView,
    ProductCreateView,
    ProductUpdateView,
    ProductArchiveView,
    OrderCreateView,
    OrderUpdateView,
    OrderCancelView,
    ProductsDataExportView,
    OrdersDataExportView,
    ProductViewSet,
)


app_name = 'shopapp'

routers = DefaultRouter()
routers.register("products", ProductViewSet)

urlpatterns = [
     # Когда кэширование не настроено в классе
     # path('', cache_page(60 * 3)(MainView.as_view()),
     #      name='main'),
     path('', MainView.as_view(),
          name='main'),

     path('api/', include(routers.urls)),
     path('products/', ProductsListView.as_view(),
          name='products_list'),
     path('products/export/', ProductsDataExportView.as_view(),
          name='products-export'),
     path('products/create/', ProductCreateView.as_view(),
          name='product_create'),
     path('products/<int:pk>/', ProductDetailsView.as_view(),
          name='product_details'),
     path('products/<int:pk>/update/', ProductUpdateView.as_view(),
          name='product_update'),
     path('products/<int:pk>/archive/', ProductArchiveView.as_view(),
          name='product_archive'),

     path('orders/', OrderListView.as_view(),
          name='orders_list'),
     path('orders/export/', OrdersDataExportView.as_view(),
          name='orders-export'),
     path('orders/create/', OrderCreateView.as_view(),
          name='order_create'),
     path('orders/<int:pk>/', OrderDetailView.as_view(),
          name='order_details'),
     path('orders/<int:pk>/update/', OrderUpdateView.as_view(),
          name='order_update'),
     path('orders/<int:pk>/delete/', OrderCancelView.as_view(),
          name='order_cancel'),
]
