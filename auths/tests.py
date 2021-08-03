from django.urls import reverse
from django.contrib import auth
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
            email='test@user.com', username='Testuser', first_name='Test',
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

    def test_create_user(self):
        response_create = self.client.post('/api/auth/register/', data=self.user_dict())
        self.assertEqual(response_create.status_code, 201)
        assert User.objects.filter(username=self.user_dict()['username'].lower()).count() == 1

        email_verification_url = response_create.data['email_verification_url']
        response_verify = self.client.get(email_verification_url)
        self.assertEqual(response_verify.status_code, 204)
        assert User.objects.filter(email_confirmed=True).count() == 1

    def test_login(self):
        rv = self.client.post('/api/auth/register/', data=self.user_dict())
        rv_login = self.client.post('/api/auth/login/', data=dict(email=self.user_dict()['email'],
                                                                  password=self.user_dict()['password']))
        self.assertEqual(rv_login.status_code, 200)
        self.assertContains(rv_login, 'refresh')
        self.assertContains(rv_login, 'access')

        #check if token works
        auth_headers = {'HTTP_AUTHORIZATION': 'Bearer ' + rv_login.data['access']}
        rv_login_2 = self.client.get('/api/auth/user/', **auth_headers)
        self.assertEqual(rv_login_2.status_code, 200)


    def test_change_password(self):
        rv = self.client.post('/api/auth/register/', data=self.user_dict())
        rv_forgot_pwd = self.client.post('/api/auth/forgot_password/', data=dict(email=self.user_dict()['email']))
        self.assertEqual(rv_forgot_pwd.status_code, 200)

        password_reset_url = rv_forgot_pwd.data['password_reset_url']
        rv_change_pwd = self.client.post('/api/auth/reset_password/',
                                         data=dict(uid='MTY', token=password_reset_url.split('token=')[1],
                                                   password='NewPassword101'))
        self.assertEqual(rv_change_pwd.status_code, 204)

        rv_login = self.client.post('/api/auth/login/', data=dict(email=self.user_dict()['email'],
                                                                  password='NewPassword101'))
        self.assertEqual(rv_login.status_code, 200)











