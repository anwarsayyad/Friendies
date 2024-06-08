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

class FreindsSerialiser(serializers.ModelSerializer):
    to = UserSerializers(read_only=True)
    req_from = UserSerializers(read_only=True)

    class Meta:
        model = Friends
        fields = ['id','to', 'req_from', 'status', 'timestamp']
        read_only_fields = ['id']

class FriendsSerializersReq(serializers.ModelSerializer):
    requests_to = UserSerilaizersForFriends(many=False, required=True)

    class Meta:
        model = Friends
        fields = ['id', 'requests_to',]
        read_only_fields = ['id']

class FrindsSerializerRes(serializers.Serializer):
    action = serializers.ChoiceField(choices=[('accept', 'accept'), ('rejected', 'rejected')])

    def update(self, instace, validated_data):
        action = validated_data.get('action')
        print(validated_data)
        if action == 'accept':
            instace.status = 'accepted'
            instace.save()
            instace.to.friends.add(instace.req_from)
        elif action == 'rejected':
            instace.status = 'rejected'
            instace.save()
        return instace

