"""
views for the user API
"""

from rest_framework import generics, authentication, permissions
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings

from user.serializer import (
    UserSerializers,
    AuthTokenSerialzier,
)


class CreateUserView(generics.CreateAPIView):
    """API view for creating new User in the System"""
    serializer_class = UserSerializers


class CreateTokenView(ObtainAuthToken):
    """Create a new auth token for user."""
    serializer_class = AuthTokenSerialzier
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES


class MangerUserView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializers
    # authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        """Retrive and return the authenticated user."""
        return self.request.user
