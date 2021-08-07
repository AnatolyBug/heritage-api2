from rest_framework.test import APITestCase, override_settings


from auths.models import User


@override_settings(TEST=True)
class UsersViewsTest(APITestCase):

    def user1(self):
        return dict(email='test@user.com', username='Testuser', first_name='Test',
                    last_name='User', password='Testuser123', bio='abc')
    def user2(self):
        return dict(email='test2@user.com', username='Testuser2', first_name='Test2',
                    last_name='User2', password='Testuser123', bio='abc2')

    def setUp(self):
        self.client.post('/api/auth/register/', data=self.user1())
        self.client.post('/api/auth/register/', data=self.user2())
        rv1 = self.client.post('/api/auth/login/', data=dict(email=self.user1()['email'],
                                                            password=self.user1()['password']))
        rv2 = self.client.post('/api/auth/login/', data=dict(email=self.user2()['email'],
                                                             password=self.user2()['password']))

        self.auth1 = {'HTTP_AUTHORIZATION': 'Bearer ' + rv1.data['access']}
        self.auth2 = {'HTTP_AUTHORIZATION': 'Bearer ' + rv2.data['access']}

    def test_follow(self):
        pass

