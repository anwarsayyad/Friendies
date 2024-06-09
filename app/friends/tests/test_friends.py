"""Test for API related frieds"""

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from core import models

FREIENDS_SEND_URL = reverse('friends:friendship-send')
FRIEDS_LIST = reverse('friends:friendship-list-accepted')
FRIEND_LIST_PENDING = reverse('friends:friendship-list-pending')
USER_SERACH = reverse('friends:search-user-list')


def create_request(to, req_from):
    req = models.Friends.objects.create(to=to, req_from=req_from)
    return req


def get_respond_url(pk):
    return reverse('friends:friendship-respond', kwargs={'pk': pk})


def create_user(**params):
    user = get_user_model().objects.create_user(**params)
    return user


class PublicFriendReqAPITest(TestCase):
    """Test cases for the public requests"""

    def setUp(self):
        self.client = APIClient()

    def test_friendreq_public(self):
        """Test authentication required"""

        res = self.client.post(
            FREIENDS_SEND_URL,
            {'requests_to': {'name': 'user2', 'email': 'user2@exm.com'}},
            format='json'
        )

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)


class PrivateFriendReq(TestCase):
    """Testing private access of API"""

    def setUp(self) -> None:
        self.client = APIClient()
        self.user1 = create_user(
            email='user1@exm.com',
            password='exm1234G',
            name='user1'
        )
        self.user2 = create_user(
            email='user2@exm.com',
            password='Test123',
            name='user2'
        )
        self.user3 = create_user(
            email='user3@exm.com',
            password='Test123',
            name='user3'
        )
        self.user4 = create_user(
            email='user4@exm.com',
            password='Test123',
            name='user4'
        )
        self.user5 = create_user(
            email='user5@exm.com',
            password='Test123',
            name='user5'
        )

    def test_send_friend_freq_and_too_many_req(self):
        self.client.force_authenticate(self.user1)
        payload = {
            'requests_to': {'name': 'user2', 'email': 'user2@exm.com'}
        }
        payload1 = {
            'requests_to': {'name': 'user5', 'email': 'user5@exm.com'}
        }
        payload2 = {
            'requests_to': {'name': 'user3', 'email': 'user3@exm.com'}
        }
        payload3 = {
            'requests_to': {'name': 'user4', 'email': 'user4@exm.com'}
        }
        res = self.client.post(FREIENDS_SEND_URL, payload, format='json')
        res1 = self.client.post(FREIENDS_SEND_URL, payload1, format='json')
        res2 = self.client.post(FREIENDS_SEND_URL, payload2, format='json')
        res3 = self.client.post(FREIENDS_SEND_URL, payload3, format='json')
        # time.sleep(60)
        # res4 = self.client.post(FREIENDS_SEND_URL, payload, format='json')

        # self.assertEqual(res4.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(res2.status_code, status.HTTP_201_CREATED)
        self.assertEqual(res1.status_code, status.HTTP_201_CREATED)
        self.assertEqual(res3.status_code, status.HTTP_429_TOO_MANY_REQUESTS)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        frnd = models.Friends.objects.filter(req_from=self.user1)
        self.assertEqual(frnd.count(), 3)
        exists = frnd.filter(
            req_from_id=self.user1.id,
            to_id=self.user2.id,
        ).exists()
        self.assertTrue(exists)

    def test_friend_request_accept_or_reject(self):
        req = create_request(self.user2, self.user1)
        self.client.force_authenticate(self.user2)
        url = get_respond_url(pk=req.id)
        data = {
            'action': 'accept'
        }
        res = self.client.post(url, data, format='json')
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        frnd = models.User.objects.get(id=self.user1.id)
        self.assertEqual(
            frnd.friends.get(id=self.user2.id).name,
            self.user2.name
        )
        payload = {
            'requests_to': {'name': 'user2', 'email': 'user2@exm.com'}
        }
        res = self.client.post(FREIENDS_SEND_URL, payload, format='json')
        self.assertEqual(res.status_code, status.HTTP_406_NOT_ACCEPTABLE)

    def test_friend_list(self):
        """Test to check friends list of the user After request is accepted"""
        req1 = create_request(self.user2, self.user1)
        req2 = create_request(self.user3, self.user1)
        req3 = create_request(self.user4, self.user1)

        count = models.User.objects.get(id=self.user1.id).friends.count()
        self.assertEqual(count, 0)
        data = {
            'action': 'accept'
        }
        users = {
            req1: self.user2,
            req2: self.user3,
            req3: self.user4,
        }
        for req, user in users.items():
            self.client.force_authenticate(user)
            url = get_respond_url(pk=req.id)
            res = self.client.post(url, data, format='json')
            exists = models.User.objects.get(id=self.user1.id).friends.filter(
                id=user.id
            ).exists()
            self.assertTrue(exists)
            self.assertEqual(res.status_code, status.HTTP_200_OK)
            self.client.logout()

        count = models.User.objects.get(id=self.user1.id).friends.count()
        self.assertEqual(count, 3)

        self.client.force_authenticate(self.user1)
        res = self.client.get(FRIEDS_LIST)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_pending_request(self):
        create_request(self.user1, self.user2)
        create_request(self.user1, self.user3)
        create_request(self.user1, self.user4)

        self.client.force_authenticate(self.user1)
        res = self.client.get(FRIEND_LIST_PENDING)

        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_user_search(self):
        self.client.force_authenticate(self.user1)
        res = self.client.get(USER_SERACH, {'search': 'us'})
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data['results']), 5)

    def test_email_search(self):
        self.client.force_authenticate(self.user1)

        res = self.client.get(USER_SERACH, {'search': 'user5@exm.com'})
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data['results'][0]['name'], 'user5')
