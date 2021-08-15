from rest_framework.test import APITestCase, override_settings
from django.db import connection, transaction
import pandas as pd
import json


from auths.models import User


@override_settings(TEST=True)
class UsersViewsTest(APITestCase):

    def setUp(self):
        user = dict(id=100, email='test@user.com', username='Testuser', first_name='Test',
                    last_name='User', password='Testuser123', bio='abc')
        rv = self.client.post('/api/auth/register/', data=user)
        rv = self.client.post('/api/auth/login/', data=dict(email=user['email'], password=user['password']))
        self.auth_headers = {'HTTP_AUTHORIZATION': 'Bearer ' + rv.data['access']}
        #self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + rv.data['access'])

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
        return dict(email=f'admin@example.com', username=f'adminuser', password='TestPassword123',
                    first_name='Admin', last_name='Adminov', bio='')

    def user_updated(self):
        return dict(email='newemail@user.com', username='newusername', first_name='New',
                            last_name='User', bio='')


    def test_list(self):
        rv = self.client.get('/api/users/', **self.auth_headers)
        self.assertEqual(rv.status_code, 200)
        self.assertFalse(rv.data['previous_page'])
        self.assertTrue(rv.data['next_page'])

        rv = self.client.get('/api/users/?page=2', **self.auth_headers)
        self.assertEqual(rv.status_code, 200)
        self.assertTrue(rv.data['previous_page'])
        self.assertFalse(rv.data['next_page'])

    def test_retrieve(self):
        #User 444 id shouldn't exist
        rv = self.client.get('/api/users/444/', **self.auth_headers)
        self.assertEqual(rv.status_code, 404)

        id = User.objects.get(username='username1').id
        rv = self.client.get('/api/users/'+str(id)+'/', **self.auth_headers)
        self.assertEqual(rv.status_code, 200)

    def test_superuser_update(self):
        rv = self.client.post('/api/auth/register/', data=self.superuser())
        rv = self.client.post('/api/auth/login/', data=dict(email=self.superuser()['email'],
                                                            password=self.superuser()['password']))
        superuser = User.objects.get(username=self.superuser()['username'])
        superuser.user_role = 'superuser'
        superuser.save()
        auth_headers = {'HTTP_AUTHORIZATION': 'Bearer ' + rv.data['access']}

        rv = self.client.post('/api/auth/login/', data=dict(email=self.superuser()['email'],
                                                            password=self.superuser()['password']), **auth_headers)
        self.assertEqual(rv.status_code, 200)

        user_updated_bad = dict(email='newemail@user.com', username='username1', first_name='New',
                    last_name='User', bio='')

        #https://stackoverflow.com/questions/30671808/django-rest-framework-empty-request-data
        rv = self.client.put('/api/users/100/', data=json.dumps(user_updated_bad), content_type='application/json',
                                     **auth_headers)
        self.assertEqual(rv.status_code, 404)

        #username already exists
        id = User.objects.get(username='username0').id
        query = str(User.objects.all().query)
        df = pd.read_sql_query(query, connection)
        with transaction.atomic():
            rv = self.client.put('/api/users/'+str(id)+'/', data=json.dumps(user_updated_bad), content_type='application/json',
                             **auth_headers)
        self.assertEqual(rv.status_code, 400)
        self.assertContains(rv, 'already exists', status_code=400)

        user_updated = self.user_updated()
        rv = self.client.put('/api/users/'+str(id)+'/', data=json.dumps(user_updated), content_type='application/json',
                             **auth_headers)
        self.assertEqual(rv.status_code, 200)
        self.assertContains(rv, 'created_date')
        assert User.objects.filter(username='newusername').count() == 1

    def test_superuser_destroy(self):
        u = self.user_updated()
        u['password'] = 'TestPassword123'
        rv = self.client.post('/api/auth/register/', data=u)
        id = rv.data['id']
        rv = self.client.post('/api/auth/register/', data=self.superuser())
        rv = self.client.post('/api/auth/login/', data=dict(email=self.superuser()['email'],
                                                            password=self.superuser()['password']))
        superuser = User.objects.get(username=self.superuser()['username'])
        superuser.user_role = 'superuser'
        superuser.save()
        auth_headers = {'HTTP_AUTHORIZATION': 'Bearer ' + rv.data['access']}

        rv = self.client.delete('/api/users/'+str(id)+'/', **auth_headers)
        assert User.objects.filter(username=self.user_updated()['username'],
                                   is_active=False).count() == 1


















