"""Views for the friends API"""
from datetime import timezone, timedelta, datetime

from rest_framework import (
    viewsets,
    mixins,
    status
)

from core import models

from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import Friends

from .serialziers import FriendsSerializersReq



class FriendsViewSet(
    viewsets.GenericViewSet
):
    """Class for the Frind API view set"""
    queryset = Friends.objects.all()
    serializer_class = FriendsSerializersReq
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    @action(detail=False, methods=['post'], url_name='send', url_path='send')
    def send(self, request):
        """Sending request to friend"""
        req_from = request.user
        to_data = request.data.get('requests_to')
        print(request.data)
        to = models.User.objects.get(email = to_data['email'])

        one_min_ago = datetime.now(tz=timezone.utc) - timedelta(minutes=1)
        recent_requests = Friends.objects.filter(
            req_from=req_from,
            timestamp__gte=one_min_ago,
        ).count()
        if recent_requests >= 3:
            return Response({'error': 'Too Many requests please try agin later'}, status=status.HTTP_429_TOO_MANY_REQUESTS)

        freindship, created = Friends.objects.get_or_create(req_from=req_from,to=to)

        if not created:
            return Response({'error': 'Friend request already sent'}, status=status.HTTP_400_BAD_REQUEST)

        return Response(FriendsSerializersReq(freindship).data, status=status.HTTP_201_CREATED)
