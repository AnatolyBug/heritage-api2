from rest_framework.test import APITestCase, override_settings

from auths.models import User


@override_settings(TEST=True)
class UsersViewsTest(APITestCase):

    def setUp(self):
        user = dict(email='test@user.com', username='Testuser', first_name='Test',
                    last_name='User', password='Testuser123', bio='abc')
        rv = self.client.post('/api/auth/register/', data=user)
        rv = self.client.post('/api/auth/login/', data=dict(email=user['email'], password=user['password']))

        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + rv.data['access'])