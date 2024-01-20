from django.test import TestCase
from restaurant.models import Menu
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from restaurant.serializers import MenuSerializer
from rest_framework.test import APIClient
from restaurant.views import MenuItemView
from django.urls import reverse


class MenuViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.token = Token.objects.create(user=self.user)

        self.pasta = Menu.objects.create(title='Pasta', price=12.99, inventory=30)
        self.momo = Menu.objects.create(title='Momo', price=6.99, inventory=200)

    def test_get_all(self):
        test_menu_objects = Menu.objects.filter(title__in=['Pasta', 'Momo'])
        serialized_data = MenuSerializer(test_menu_objects, many=True)

        client = APIClient()
        url = reverse('menu')

        client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')
        response = client.get(url)

        self.assertEqual(response.data, serialized_data.data)
