from rest_framework.test import APITestCase, override_settings
#from django.db import connection
#import pandas as pd


from auths.models import User
from relationships.models import Relationships


@override_settings(TEST=True)
class UsersViewsTest(APITestCase):

    def user1(self):
        return dict(email='test@user.com', username='Testuser', first_name='Test', id=3,
                    last_name='User', password='Testuser123', bio='abc')
    def user2(self):
        return dict(email='test2@user.com', username='Testuser2', first_name='Test2', id=4,
                    last_name='User2', password='Testuser123', bio='abc2')
    def superuser(self):
        return dict(email=f'admin@example.com', username=f'adminuser', password='TestPassword123',
                            first_name='Admin', last_name='Adminov', bio='')

    def setUp(self):
        rv = self.client.post('/api/auth/register/', data=self.user1())
        rv2 = self.client.post('/api/auth/register/', data=self.user2())
        self.id1 = rv.data['id']
        self.id2 = rv2.data['id']
        rv1 = self.client.post('/api/auth/login/', data=dict(email=self.user1()['email'],
                                                             password=self.user1()['password']))
        rv2 = self.client.post('/api/auth/login/', data=dict(email=self.user2()['email'],
                                                             password=self.user2()['password']))
        self.user1_db = User.objects.get(username=self.user1()['username'].lower())
        self.user2_db = User.objects.get(username=self.user2()['username'].lower())

        self.auth1 = {'HTTP_AUTHORIZATION': 'Bearer ' + rv1.data['access']}
        self.auth2 = {'HTTP_AUTHORIZATION': 'Bearer ' + rv2.data['access']}

    def test_follow(self):
        #Cannot follow yourself
        rv = self.client.post('/api/relationships/', data={'to_user': self.id1,
                                                                  'status': 'FOLLOW'}, **self.auth1)
        self.assertEqual(rv.status_code, 204)
        self.assertEqual(rv.data['status'], 'SELF')

        #Bad rel status
        rv = self.client.post('/api/relationships/', data={'to_user': self.id2,
                                                                  'status': 'BAD_STATUS'}, **self.auth1)
        self.assertEqual(rv.status_code, 400)

        rv = self.client.post('/api/relationships/', data={'to_user': self.id2,
                                                                  'status': 'FOLLOW'}, **self.auth1)
        self.assertEqual(rv.status_code, 201)
        assert Relationships.objects.filter(from_user_id=self.user1_db, to_user_id=self.user2_db).count() == 1
        assert Relationships.objects.filter(from_user_id=self.user1_db,
                                            to_user_id=self.user2_db).first().status == 'FOLLOW'

        rv = self.client.post('/api/relationships/', data={'to_user': self.id2,
                                                                  'status': 'UNFOLLOW'}, **self.auth1)
        self.assertEqual(rv.status_code, 200)
        assert Relationships.objects.filter(from_user_id=self.user1_db, to_user_id=self.user2_db).count() == 1
        assert Relationships.objects.filter(from_user_id=self.user1_db,
                                            to_user_id=self.user2_db).first().status == 'UNFOLLOW'

        rv = self.client.post('/api/relationships/', data={'to_user': self.id2,
                                                                  'status': 'BLOCK'}, **self.auth1)
        self.assertEqual(rv.status_code, 200)
        assert Relationships.objects.filter(from_user_id=self.user1_db, to_user_id=self.user2_db).count() == 1
        assert Relationships.objects.filter(from_user_id=self.user1_db,
                                            to_user_id=self.user2_db).first().status == 'BLOCK'

        rv = self.client.post('/api/relationships/', data={'to_user': self.id2, 'status': 'UNBLOCK'}, **self.auth1)
        self.assertEqual(rv.status_code, 200)
        assert Relationships.objects.filter(from_user_id=self.user1_db, to_user_id=self.user2_db).count() == 1
        assert Relationships.objects.filter(from_user_id=self.user1_db,
                                            to_user_id=self.user2_db).first().status == 'UNBLOCK'


    def test_get(self):
        #User 1 -> User 2
        rv = self.client.get('/api/relationships/', **self.auth1)
        self.assertEqual(rv.status_code, 200)
        self.assertFalse(rv.data['relationships_from_user'])
        self.assertFalse(rv.data['relationships_to_user'])

        rv = self.client.post('/api/relationships/', data={'to_user': self.id2, 'status': 'FOLLOW'}, **self.auth1)
        rv = self.client.get('/api/relationships/', **self.auth1)
        self.assertEqual(rv.status_code, 200)
        self.assertContains(rv, self.user2()['username'].lower())

        #User 2 -> User 1
        rv = self.client.get('/api/relationships/', **self.auth2)
        self.assertEqual(rv.status_code, 200)
        self.assertFalse(rv.data['relationships_from_user'])
        assert self.user1()['username'].lower() in str(rv.data['relationships_to_user'])

    def test_delete(self):
        rv = self.client.post('/api/relationships/', data={'to_user': self.id2, 'status': 'FOLLOW'}, **self.auth1)
        rv = self.client.get('/api/relationships/', **self.auth1)
        rel_id = rv.data['relationships_from_user'][0]['id']
        rv = self.client.delete('/api/relationships/'+str(rel_id)+'/', **self.auth2)
        self.assertEqual(rv.status_code, 400)

        #register login superuser
        rv = self.client.post('/api/auth/register/', data=self.superuser())
        rv = self.client.post('/api/auth/login/', data=dict(email=self.superuser()['email'],
                                                            password=self.superuser()['password']))
        superuser = User.objects.get(username=self.superuser()['username'])
        superuser.user_role = 'superuser'
        superuser.save()
        super_auth_headers = {'HTTP_AUTHORIZATION': 'Bearer ' + rv.data['access']}

        #Delete relationship
        rv = self.client.delete('/api/relationships/' + str(rel_id) + '/', **super_auth_headers)
        self.assertEqual(rv.status_code, 204)
        assert Relationships.objects.filter().count() == 0

        #Create relationship again and delete user
        rv = self.client.post('/api/relationships/', data={'to_user': self.id2, 'status': 'FOLLOW'}, **self.auth1)
        rv = self.client.delete('/api/users/' + str(self.id2) + '/', **super_auth_headers)

        #query = str(User.objects.all().query)
        #df = pd.read_sql_query(query, connection)

        rv = self.client.get('/api/relationships/', **self.auth1)
        self.assertEqual(rv.status_code, 200)
        self.assertFalse(rv.data['relationships_from_user'])
        self.assertFalse(rv.data['relationships_to_user'])






