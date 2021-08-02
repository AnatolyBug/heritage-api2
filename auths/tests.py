from django.urls import reverse
from django.test import TestCase, override_settings
import json

from auths.models import User


@override_settings(TEST=True)
class UserViewsTest(TestCase):

    def bad_user_dict(self):
        return dict(
            email='bad@user.com', username='', first_name='Test', last_name='User', password='', bio='abc'
        )

    def user_dict(self):
        return dict(
            email='test@user.com', username='testuser', first_name='Test',
            last_name='User', password='Testuser123', bio='abc')

    @classmethod
    def setUpTestData(cls):
        # Create 15 Users for pagination tests
        number_of_users = 15

        for user_id in range(number_of_users):
            User.objects.create(
                email=f'test@example.com {str(user_id)}',
                username=f'Username {str(user_id)}',
                first_name=f'First Name {str(user_id)}',
                last_name=f'Surname {str(user_id)}',
                password='TestPassword123'
            )

    @override_settings()
    def test_create_user(self):
        response = self.client.post('/api/auth/register/', data=self.user_dict())
        self.assertEqual(response.status_code, 200)
