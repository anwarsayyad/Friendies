"""
Test for models
"""
from unittest.mock import patch

from django.test import TestCase
from django.contrib.auth import get_user_model

from core import models

def create_user(email='user@example.com', password='testPass1234'):
    """create and return new user"""
    return get_user_model().objects.create_user(email, password)

class ModelTests(TestCase):
    """Test Model"""

    def test_create_user_with_email(self):
        """Test creating a user with an email is successful."""
        email = 'test@example.com'
        password = 'testpass123'
        user = get_user_model().objects.create_user(
            email=email,
            password=password
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_user_mail_insensitive(self):
        """Test email is insesitive"""
        sample_mail = [
            ['user1@Example.com', 'user1@example.com'],
            ['UseR2@exAmpLe.com', 'user2@example.com'],
            ['USER3@EXAMPLE.COM', 'user3@example.com'],
        ]

        for email, expected in sample_mail:
            user = get_user_model().objects.create_user(email, 'Sample1234')
            self.assertEqual(user.email, expected)

