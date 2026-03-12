from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model


class UsersManagersTests(TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        User = get_user_model()
        cls.user = User.objects.create_user(
            username='Test',
            email="normal@user.com",
            password='bar',
        )
        cls.superuser = User.objects.create_superuser(
            username='SuperTest',
            email="super@user.com",
            password='bar',
        )

    @classmethod
    def tearDownClass(cls) -> None:
        cls.user.delete()
        cls.superuser.delete()

    def test_create_user(self):
        self.assertEqual(self.user.username, "Test")
        self.assertEqual(self.user.email, "normal@user.com")
        self.assertTrue(self.user.is_active)
        self.assertFalse(self.user.is_staff)
        self.assertFalse(self.user.is_superuser)

    def test_create_superuser(self):
        self.assertEqual(self.superuser.username, "SuperTest")
        self.assertEqual(self.superuser.email, "super@user.com")
        self.assertTrue(self.superuser.is_active)
        self.assertTrue(self.superuser.is_staff)
        self.assertTrue(self.superuser.is_superuser)


class GetCookieViewTestCase(TestCase):
    def test_get_cookie_view(self):
        response = self.client.get(reverse('accounts:cookie-get'))
        self.assertContains(response, 'Cookie value')


class FooBarViewTest(TestCase):
    def test_foo_bar_view(self):
        response = self.client.get(reverse('accounts:foo-bar'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.headers['content-type'], 'application/json',
        )
        expected_data = {'foo': 'bar', 'spam': 'eggs'}
        self.assertJSONEqual(response.content, expected_data)
