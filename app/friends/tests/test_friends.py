"""Test for API related frieds"""

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from core import models
from friends.serialziers import FriendsSerializersReq

FREIENDS_SEND_URL = reverse('friends:friendship-send')
# FREIENDS_RESPOND_URL = reverse('friends:friendReq-respond')

def create_user(**params):
    user = get_user_model().objects.create_user(**params)
    return user

class PublicFriendReqAPITest(TestCase):
    """Test cases for the public requests"""

    def setUp(self):
        self.client = APIClient()

    def test_friendreq_public(self):
        """Test authentication required"""

        res = self.client.post(FREIENDS_SEND_URL, {'requests_to': {'name': 'user2', 'email': 'user2@exm.com'}}, format='json')
        # res1 = self.client.post(FREIENDS_RESPOND_URL, {})

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)
        # self.assertEqual(res1.status_code, status.HTTP_400_BAD_REQUEST)


class PrivateFriendReq(TestCase):
    """Testing private access of API"""

    def setUp(self) -> None:
        self.client = APIClient()
        self.user1 = create_user(email='user1@exm.com', password='exm1234G', name='user1')
        self.user2 = create_user(email='user2@exm.com', password='Test123', name='user2')
        self.user3 = create_user(email='user3@exm.com', password='Test123', name='user3')
        self.user4 = create_user(email='user4@exm.com', password='Test123', name='user4')

    def test_send_friend_freq(self):
        self.client.force_authenticate(self.user1)
        payload = {
            'requests_to': {'name': 'user2', 'email': 'user2@exm.com'}
        }

        res = self.client.post(FREIENDS_SEND_URL, payload, format='json')

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        frnd = models.Friends.objects.filter(req_from = self.user1)
        self.assertEqual(frnd.count(), 1)
        exists = frnd.filter(
            req_from_id=self.user1.id,
            to_id=self.user2.id,
        ).exists()
        self.assertTrue(exists)