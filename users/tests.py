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

    @classmethod
    def setUpTestData(cls):
        # Create 15 Users for pagination tests
        number_of_users = 25

        for user_id in range(number_of_users):
            User.objects.create(email=f'test@example.com {str(user_id)}',
                                username=f'Username {str(user_id)}',
                                first_name=f'First Name {str(user_id)}',
                                last_name=f'Surname {str(user_id)}',
                                password='TestPassword123')

    def test_list(self):
        rv = self.client.get('/api/users/')
        self.assertEqual(rv.status_code, 200)
        self.assertFalse(rv.data['previous_page'])
        self.assertTrue(rv.data['next_page'])

        #next_page = rv.data['next_page']
        #rv = self.client.get(next_page)
        #self.assertEqual(rv.status_code, 200)

    def test_retrieve(self):
        #User 100 id shouldn't exist
        rv = self.client.get('/api/users/100/')
        self.assertEqual(rv.status_code, 204)
