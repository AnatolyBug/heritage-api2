from rest_framework.test import APITestCase, override_settings
from auths.models import User


@override_settings(TEST=True)
class UsersViewsTest(APITestCase):

    def setUp(self):
        self.superuser = dict(email='admin@user.com', username='Adminuser', password='Adminuser123')
        rv = self.client.post('/api/auth/register/', data=self.superuser)
        email_verification_url = rv.data['email_verification_url']
        response_verify = self.client.get(email_verification_url, follow=False)
        rv = self.client.post('/api/auth/login/', data=dict(email=self.superuser['email'],
                                                            password=self.superuser['password']))
        #self.auth_headers = {'HTTP_AUTHORIZATION': 'Bearer ' + rv.data['access']}
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + rv.data['access'])

    @classmethod
    def setUpTestData(cls):
        number_of_users = 2
        for user_id in range(number_of_users):
            User.objects.create(email=f'test{str(user_id)}@example.com',
                                username=f'Username{str(user_id)}'.lower(),
                                first_name=f'First Name {str(user_id)}',
                                last_name=f'Surname {str(user_id)}',
                                password='TestPassword123')

    '''
    def test_superuser_update(self):
        superuser = User.objects.get(username=self.superuser['username'])
        superuser.is_staff = True
        superuser.save()

        rv = self.client.post('/api/auth/login/', data=dict(email=self.superuser['email'],
                                                            password=self.superuser['password']), **auth_headers)
        self.assertEqual(rv.status_code, 200)

        user_updated_bad = dict(email='newemail@user.com', username='username1', first_name='New',
                                last_name='User', bio='')

        # https://stackoverflow.com/questions/30671808/django-rest-framework-empty-request-data
        rv = self.client.put('/api/users/100/', data=json.dumps(user_updated_bad), content_type='application/json',
                             **auth_headers)
        self.assertEqual(rv.status_code, 404)

        # username already exists
        id = User.objects.get(username='username0').id
        query = str(User.objects.all().query)
        df = pd.read_sql_query(query, connection)
        with transaction.atomic():
            rv = self.client.put('/api/users/' + str(id) + '/', data=json.dumps(user_updated_bad),
                                 content_type='application/json',
                                 **auth_headers)
        self.assertEqual(rv.status_code, 400)
        self.assertContains(rv, 'already exists', status_code=400)

        user_updated = self.user_updated()
        rv = self.client.put('/api/users/' + str(id) + '/', data=json.dumps(user_updated), content_type='application/json',
                             **auth_headers)
        self.assertEqual(rv.status_code, 200)
        self.assertContains(rv, 'created_date')
        assert User.objects.filter(username='newusername').count() == 1
    '''


    def test_superuser_destroy(self):
        superuser = User.objects.get(username=self.superuser['username'].lower())
        superuser.is_staff = True
        superuser.save()
        rv = self.client.get('/api/users/')
        for user in rv.data['data']:
            if user['username'] == 'username0':
                u = user
                break
            else:
                u = None
        assert u

        rv = self.client.delete('/api/admins/users/' + str(u['id']) + '/')
        self.assertEqual(rv.status_code, 204)
        assert User.objects.filter(username=u['username'], is_active=False).count() == 1
