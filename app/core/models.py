"""
Here will be all the models of our project will be present
"""

from django.db import  models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)


from django.conf import settings

STATUS_CHOICES = {
    'pending': 'pending',
    'accepted': 'accepted',
    'rejected': 'rejected',
}

class UserManager(BaseUserManager):
    """Manging Users"""

    def create_user(self, email, password=None, **extra_fields):
        """Create, save and return a new user"""
        if not email:
            raise ValueError('User must have an email adddress.')
        email = self.normalize_email(email).lower()
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password):
        """Create and return new super user"""
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    """DJnago default user"""
    email = models.EmailField(max_length=225, unique=True)
    name = models.CharField(max_length=225)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'

class Friends(models.Model):
    """
    Model for the Friends that will be
    Having the request sent and recived with status and time
    stamp
    """
    to = models.ForeignKey(User, related_name='requests_to', on_delete=models.CASCADE)
    req_from = models.ForeignKey(User, related_name='requests_recived', on_delete=models.CASCADE)
    status = models.CharField(max_length=255, choices=STATUS_CHOICES, default='pending')
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('to', 'req_from')

