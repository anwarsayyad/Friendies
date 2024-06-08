"""Friends API serializers"""

from rest_framework import serializers

from core.models import (
    Friends
)
from user.serializer import UserSerializers


class UserSerilaizersForFriends(UserSerializers):
    """Seriaizers for Friends API"""

    class Meta(UserSerializers.Meta):
        fields = ['name', 'email']

class FriendsSerializersReq(serializers.ModelSerializer):
    to = UserSerilaizersForFriends(many=False, required=True)

    class Meta:
        model = Friends
        fields = ['id', 'to', 'status']
        read_only_fields = ['id']
