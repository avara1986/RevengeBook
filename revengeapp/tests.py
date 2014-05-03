from django.contrib.auth import get_user_model
from django.core.urlresolvers import reverse
from django.test import TestCase
from django.test.client import Client


class RevengeBookTestCase(TestCase):

    def setUp(self):
        self.client = Client()

    def create_user(self, username, password):
        User = get_user_model()
        user, is_created = User.objects.get_or_create(username=username)
        if is_created:
            user.set_password(password)
            user.save()
        return user

    def delete_user(self, username):
        User = get_user_model()
        user = User.objects.get(username=username)
        user.delete()

    def login(self, username, password):
        is_login = self.client.login(username=username, password=password)
        self.assertEqual(is_login, True)

    def test_get_200(self):
        # index view
        index_url = reverse('index')
        index_res = self.client.get(index_url)
        self.assertEqual(index_res.status_code, 200)

        # revengepanel view
        revengepanel_url = reverse('RevengePanel')
        revengepanel_res = self.client.get(revengepanel_url)
        self.assertEqual(revengepanel_res.status_code, 302)

        # search friend view
        search_friend_url = reverse('searchFriend')
        search_friend_res = self.client.get(search_friend_url)
        self.assertEqual(search_friend_res.status_code, 302)

        # see profile view
        see_profile_url = reverse('see_profile', kwargs={'idfriend': 1})
        see_profile_res = self.client.get(see_profile_url)
        self.assertEqual(see_profile_res.status_code, 302)

        # sign up view
        sign_up_url = reverse('sign_up')
        sign_up_res = self.client.get(sign_up_url)
        self.assertEqual(sign_up_res.status_code, 200)

        # sign out view
        sign_out_url = reverse('sign_out')
        sign_out_res = self.client.get(sign_out_url)
        self.assertEqual(sign_out_res.status_code, 302)

    def test_get_200_with_login(self):
        User = get_user_model()
        username = password = 'user1'
        self.create_user(username, password)
        self.login(username, password)
        revengepanel_url = reverse('RevengePanel')
        revengepanel_res = self.client.get(revengepanel_url)
        self.assertEqual(revengepanel_res.status_code, 200)
        self.delete_user(username)
        self.assertEqual(User.objects.filter(username=username).count(), 0)

    def test_friends(self):
        user1 = self.create_user('user1', 'user1')
        user2 = self.create_user('user2', 'user3')
        user3 = self.create_user('user3', 'user3')
        user1.friends.add(user2)
        user3.friends.add(user2)
        user2_friends = [user.username
                           for user in user2.friends.all().order_by('pk')]
        self.assertEqual(user2_friends, ['user1', 'user3'])
        self.delete_user('user1')
        self.delete_user('user2')
        self.delete_user('user3')
