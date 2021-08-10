from rest_framework.test import APITestCase, override_settings
from django.db import connection
import pandas as pd


from auths.models import User


@override_settings(TEST=True)
class UsersViewsTest(APITestCase):

    def setUp(self):
        user = dict(id=100, email='test@user.com', username='Testuser', first_name='Test',
                    last_name='User', password='Testuser123', bio='abc')
        rv = self.client.post('/api/auth/register/', data=user)
        rv = self.client.post('/api/auth/login/', data=dict(email=user['email'], password=user['password']))

        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + rv.data['access'])

    @classmethod
    def setUpTestData(cls):
        # Create 15 Users for pagination tests
        number_of_users = 25
        for user_id in range(number_of_users):
            User.objects.create(email=f'test{str(user_id)}@example.com',
                                username=f'Username{str(user_id)}'.lower(),
                                first_name=f'First Name {str(user_id)}',
                                last_name=f'Surname {str(user_id)}',
                                password='TestPassword123')

    def superuser(self):
        return dict(email=f'admin@example.com', username=f'adminuser', user_role='admin',
            password='TestPassword123', id=30)


    def test_list(self):
        rv = self.client.get('/api/users/')
        self.assertEqual(rv.status_code, 200)
        self.assertFalse(rv.data['previous_page'])
        self.assertTrue(rv.data['next_page'])

        rv = self.client.get('/api/users/?page=2')
        self.assertEqual(rv.status_code, 200)
        self.assertTrue(rv.data['previous_page'])
        self.assertFalse(rv.data['next_page'])

    def test_retrieve(self):
        #User 100 id shouldn't exist
        rv = self.client.get('/api/users/100/')
        self.assertEqual(rv.status_code, 204)

        rv = self.client.get('/api/users/username1/')
        self.assertEqual(rv.status_code, 200)

    def test_superuser_update(self):
        User.objects.create(**self.superuser())
        rv = self.client.post('/api/auth/login/', data=dict(email=self.superuser()['email'], password=self.superuser()['password']))
        #query = str(User.objects.all().query)
        #df = pd.read_sql_query(query, connection)
        self.assertEqual(rv.status_code, 200)



