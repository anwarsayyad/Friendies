"""Test for API related frieds"""

import time

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from core import models
from friends.serialziers import FriendsSerializersReq

FREIENDS_SEND_URL = reverse('friends:friendship-send')

def create_request(to,req_from):
    req = models.Friends.objects.create(to=to, req_from=req_from)
    return req

def get_respond_url(pk):
    return reverse('friends:friendship-respond', kwargs={'pk':pk})

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

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateFriendReq(TestCase):
    """Testing private access of API"""

    def setUp(self) -> None:
        self.client = APIClient()
        self.user1 = create_user(email='user1@exm.com', password='exm1234G', name='user1')
        self.user2 = create_user(email='user2@exm.com', password='Test123', name='user2')
        self.user3 = create_user(email='user3@exm.com', password='Test123', name='user3')
        self.user4 = create_user(email='user4@exm.com', password='Test123', name='user4')
        self.user5 = create_user(email='user5@exm.com', password='Test123', name='user5')

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
        res1 =  self.client.post(FREIENDS_SEND_URL, payload1, format='json')
        res2 =  self.client.post(FREIENDS_SEND_URL, payload2, format='json')
        res3 =  self.client.post(FREIENDS_SEND_URL, payload3, format='json')
        # time.sleep(60)
        # res4 = self.client.post(FREIENDS_SEND_URL, payload, format='json')

        # self.assertEqual(res4.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(res2.status_code, status.HTTP_201_CREATED)
        self.assertEqual(res1.status_code, status.HTTP_201_CREATED)
        self.assertEqual(res3.status_code, status.HTTP_429_TOO_MANY_REQUESTS)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        frnd = models.Friends.objects.filter(req_from = self.user1)
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
            'action':'accept'
        }

        res = self.client.post(url, data, format='json')
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        frnd = models.User.objects.get(id=self.user2.id)
        self.assertEqual(frnd.friends.get(id=self.user1.id).name, self.user1.name)



        payload = {
            'requests_to': {'name': 'user2', 'email': 'user2@exm.com'}
        }


        res = self.client.post(FREIENDS_SEND_URL, payload, format='json')
        self.assertEqual(res.status_code, status.HTTP_406_NOT_ACCEPTABLE)

