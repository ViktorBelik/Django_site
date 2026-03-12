from django.http import HttpRequest
from django.test import TestCase
from django.urls import reverse
from django.conf import settings
from django.contrib.auth.models import User, Permission
from .models import Product, Order
from shopapp.utils import add_two_numbers


class AddTwoNumbersTestCase(TestCase):
    def test_add_two_numbers(self):
        result = add_two_numbers(2, 3)
        self.assertEqual(result, 5)


class ProductCreateViewTastCase(TestCase):
    def test_create_product(self):
        response = self.client.post(
            reverse('shopapp:product_create'),
            {
                'name': 'Table',
                'price': '23455.5',
                'description': 'A good',
                'discount': '10',
            }
        )
        self.assertRedirects(
            response,
            '/accounts/login/?next=/shop/products/create/'
        )


class ProductDetailsViewTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.user = User.objects.create_user(
            username='bob_test',
            password='qwerty'
        )
        cls.product = Product.objects.create(
            name='Best Product',
            created_by=cls.user
        )

    @classmethod
    def tearDownClass(cls):
        cls.product.delete()
        cls.user.delete()

    def test_get_product(self):
        response = self.client.get(
            reverse('shopapp:product_details', kwargs={'pk': self.product.pk})
        )
        self.assertEqual(response.status_code, 200)

    def test_get_product_and_chek_content(self):
        response = self.client.get(
            reverse('shopapp:product_details', kwargs={'pk': self.product.pk})
        )
        self.assertContains(response, self.product.name)


class ProductsListViewTestCase(TestCase):
    fixtures = [
        'products-fixture.json',
    ]

    @classmethod
    def setUpClass(cls):
        # cls.credentials = dict(username='bob_test', password='qwerty')
        # cls.user = User.objects.create_user(**cls.credentials)
        cls.user = User.objects.create_user(
            username='bob_test',
            password='qwerty'
        )

    @classmethod
    def tearDownClass(cls):
        cls.user.delete()

    def setUp(self) -> None:
        # self.client.login(**self.credentials)
        self.client.force_login(self.user)

    def test_products(self):
        response = self.client.get(reverse('shopapp:products_list'))
        # products = Product.objects.filter(archived=False).all()
        # products_ = response.context['products']
        # for p, p_ in zip(products, products_):
        #     self.assertEqual(p.pk, p_.pk)

        self.assertQuerySetEqual(
            qs=Product.objects.filter(archived=False).all(),
            values=(p.pk for p in response.context['products']),
            transform=lambda p: p.pk
        )
        self.assertTemplateUsed(response, 'shopapp/products_list.html')


class ProductExportViewTestCase(TestCase):
    fixtures = [
        'products-fixture.json',
    ]

    @classmethod
    def setUpClass(cls):
        cls.user = User.objects.create_user(
            username='bob_test',
            password='qwerty'
        )

    @classmethod
    def tearDownClass(cls):
        cls.user.delete()

    def setUp(self) -> None:
        self.client.force_login(self.user)

    def test_get_poducts_view(self):
        response = self.client.get(
            reverse('shopapp:products-export')
        )
        self.assertEqual(response.status_code, 200)

        products = Product.objects.order_by('pk').all()
        expected_data = [
            {
                "pk": product.pk,
                "name": product.name,
                "price": product.price,
                "archived": product.archived,
            }
            for product in products
        ]
        products_data = response.json()
        self.assertEqual(
            products_data['products'],
            expected_data,
        )


class OrdersListViewTestCase(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.user = User.objects.create_user(
            username='bob_test',
            password='qwerty'
        )

    @classmethod
    def tearDownClass(cls):
        cls.user.delete()

    def setUp(self) -> None:
        self.client.force_login(self.user)

    def test_orders_view(self):
        response = self.client.get(reverse('shopapp:orders_list'))
        self.assertContains(response, 'Orders')

    def test_orders_view_not_authenticated(self):
        self.client.logout()
        response = self.client.get(reverse('shopapp:orders_list'))
        self.assertEqual(response.status_code, 302)
        self.assertIn(str(settings.LOGIN_URL), response.url)


class OrderDetailViewTestCase(TestCase):
    fixtures = [
        'orders-fixture.json',
    ]

    @classmethod
    def setUpClass(cls) -> None:
        cls.user = User.objects.create_user(
            username='bob_test',
            password='qwerty'
        )
        permission_order = Permission.objects.get(codename='view_order')
        cls.user.user_permissions.add(permission_order)

    @classmethod
    def tearDownClass(cls) -> None:
        cls.user.delete()

    def setUp(self) -> None:
        self.client.force_login(self.user)
        self.product = Product.objects.create(
            name='Best Product',
            created_by=self.user
        )
        self.order = Order.objects.create(
            delivery_address='Test the Street',
            promocode='SALE TEST',
            user=self.user,
        )
        self.order.products.add(self.product)

    def tearDown(self) -> None:
        self.order.delete()
        self.product.delete()

    def test_order_details(self):
        response = self.client.get(reverse(
            'shopapp:order_details',
            kwargs={'pk': self.order.pk}
            )
        )
        # Проверка кода ответа
        self.assertEqual(response.status_code, 200)
        # Проверка наличия адреса и промокода
        self.assertContains(response, self.order.delivery_address)
        self.assertContains(response, self.order.promocode)
        # Проверка соответствия заказа тому, который был создан
        received_data = response.context["order"].pk
        self.assertEqual(received_data, self.order.pk)


class OrdersExportTestCase(TestCase):
    fixtures = [
        'orders-fixture.json',
    ]

    @classmethod
    def setUpClass(cls) -> None:
        cls.user = User.objects.create_user(
            username='bob_test',
            password='qwerty',
            is_staff=True
        )

    @classmethod
    def tearDownClass(cls) -> None:
        cls.user.delete()

    def setUp(self) -> None:
        self.client.force_login(self.user)

    def test_get_orders_view(self):
        response = self.client.get(
            reverse('shopapp:orders-export')
        )
        self.assertEqual(response.status_code, 200)

        orders = Order.objects.order_by('pk').all()
        expected_data = [
            {
                "Order ID": order.pk,
                "Delivery address": order.delivery_address,
                "Promocode": order.promocode,
                "User ID": order.user.pk,
                "Products ID": [product.id
                                for product in order.products.all()],
            }
            for order in orders
        ]
        recived_data = response.json()
        self.assertEqual(recived_data['orders'], expected_data)
