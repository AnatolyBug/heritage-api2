from rest_framework.test import APITestCase, override_settings

from auths.models import User


@override_settings(TEST=True)
class PlacesViewsTest(APITestCase):

    def setUp(self):
        user = dict(email='test@user.com', username='Testuser', first_name='Test',
                    last_name='User', password='Testuser123', bio='abc')
        rv = self.client.post('/api/auth/register/', data=user)
        rv = self.client.post('/api/auth/login/', data=dict(email=user['email'], password=user['password']))
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + rv.data['access'])

    def hydePark(self):
        return dict(
            name="Albert Memorial",
            description="Opened in July 1872",
            address="Kensington Gardens, London W2 2UH",
            longitude=51.50725484441893,
            latitude=-0.16581613082967503
        )

    def test_create(self):
        pass