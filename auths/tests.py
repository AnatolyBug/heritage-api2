from django.test import TestCase, override_settings, TransactionTestCase
from django.db import transaction

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
        User.objects.create(email=f'alreadyexists@example.com',
                                username=f'alreadyexists',
                                first_name=f'alreadyexists',
                                last_name=f'alreadyexists',
                                password='Alreadyexists123')


    def test_create_user(self):
        response_create = self.client.post('/api/auth/register/', data=self.user_dict())
        self.assertEqual(response_create.status_code, 201)
        assert User.objects.filter(username=self.user_dict()['username'].lower()).count() == 1

        email_verification_url = response_create.data['email_verification_url']
        response_verify = self.client.get(email_verification_url)
        self.assertEqual(response_verify.status_code, 204)
        assert User.objects.filter(email_confirmed=True).count() == 1

        response_create_bad = self.client.post('/api/auth/register/', data=self.bad_user_dict())
        self.assertEqual(response_create_bad.status_code, 400)
        self.assertContains(response_create_bad, 'This field may not be blank', status_code=400)

        bad_password_user = self.bad_user_dict()
        bad_password_user['username'] = 'Bad_Password_User'
        bad_password_user['password'] = 'weak_password'
        response_create_bad = self.client.post('/api/auth/register/', data=bad_password_user)
        self.assertEqual(response_create_bad.status_code, 400)
        self.assertContains(response_create_bad, "password must contain at least an Uppercase, lowercase and a number",
                            status_code=400)

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
                                         data=dict(uid=password_reset_url.split('uid=')[1].split('&')[0],
                                                   token=password_reset_url.split('token=')[1],
                                                   password='NewPassword101'))
        self.assertEqual(rv_change_pwd.status_code, 204)

        rv_login = self.client.post('/api/auth/login/', data=dict(email=self.user_dict()['email'],
                                                                  password='NewPassword101'))
        self.assertEqual(rv_login.status_code, 200)

    def test_put(self):
        rv = self.client.post('/api/auth/register/', data=self.user_dict())
        rv_login = self.client.post('/api/auth/login/', data=dict(email=self.user_dict()['email'],
                                                                  password=self.user_dict()['password']))

        user_updated = self.user_dict()
        user_updated['username'] = 'alreadyexists'

        auth_headers = {'HTTP_AUTHORIZATION': 'Bearer ' + rv_login.data['access']}
        with transaction.atomic():
            rv_login_2 = self.client.put('/api/auth/user/', data=user_updated, content_type='application/json', **auth_headers)
        self.assertEqual(rv_login_2.status_code, 400)
        self.assertContains(rv_login_2, "Username already exists", status_code=400)

        user_updated['username'] = 'doesntexistyet'
        rv_login_3 = self.client.put('/api/auth/user/', data=user_updated, content_type='application/json',
                                     **auth_headers)
        self.assertEqual(rv_login_3.status_code, 200)
        assert User.objects.filter(username=user_updated['username'].lower()).count() == 1

    def test_destroy(self):
        rv = self.client.post('/api/auth/register/', data=self.user_dict())
        rv_login = self.client.post('/api/auth/login/', data=dict(email=self.user_dict()['email'],
                                                                  password=self.user_dict()['password']))
        auth_headers = {'HTTP_AUTHORIZATION': 'Bearer ' + rv_login.data['access']}
        rv = self.client.delete('/api/auth/user/', **auth_headers)
        self.assertEqual(rv_login.status_code, 204)


















