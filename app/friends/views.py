"""Views for the friends API"""
from datetime import timezone, timedelta, datetime

from rest_framework import (
    viewsets,
    status
)

from core import models
from django.db.models import Q
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from drf_spectacular.utils import (
    extend_schema,
    extend_schema_view,
    OpenApiExample,
    OpenApiParameter
)

from core.models import Friends

from .serialziers import (
    FriendsSerializersReq,
    FrindsSerializerRes,
    FreindsSerialiser,
    UserSerilaizersForFriends,
)


@extend_schema_view(
    send=extend_schema(
        request=FriendsSerializersReq,
        responses={201: FreindsSerialiser},
        description="Sending friend request",
    ),
    respond=extend_schema(
        request=FrindsSerializerRes,
        responses={200: FreindsSerialiser},
        description="Responding to friend request",
        examples=[
            OpenApiExample(
                "Accept Friend Request",
                value={"action": "accept"},
            ),
            OpenApiExample(
                "Rejecte Friend Request",
                value={"action": "reject"}
            ),
        ]
    ),
    list_accepted=extend_schema(
        responses={200: UserSerilaizersForFriends},
        description="Getting Friends list",
    ),
    list_pending=extend_schema(
        responses={200: FreindsSerialiser},
        description="Getting all the pending request of the user"
    )
)
class FriendsViewSet(
    viewsets.GenericViewSet
):
    """Class for the Frind API view set"""
    queryset = Friends.objects.all()
    serializer_class = FreindsSerialiser
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    @action(detail=False, methods=['post'], url_name='send', url_path='send')
    def send(self, request):
        """Sending request to friend"""
        self.serializer_class = FriendsSerializersReq
        req_from = request.user
        to_data = request.data.get('requests_to')
        to = models.User.objects.get(email=to_data['email'])
        if req_from == to:
            return Response(
                {'error': 'Not allowed to send self request'},
                status=status.HTTP_406_NOT_ACCEPTABLE
            )

        one_min_ago = datetime.now(tz=timezone.utc) - timedelta(minutes=1)
        recent_requests = Friends.objects.filter(
            req_from=req_from,
            timestamp__gte=one_min_ago,
        ).count()
        if recent_requests >= 3:
            return Response(
                {'error': 'Too Many requests please try agin later'},
                status=status.HTTP_429_TOO_MANY_REQUESTS
                )

        freindship, created = Friends.objects.get_or_create(
            req_from=req_from,
            to=to
        )

        if not created:
            return Response(
                {'error': 'Friend request already sent'},
                status=status.HTTP_400_BAD_REQUEST
            )

        return Response(
            FreindsSerialiser(freindship).data,
            status=status.HTTP_201_CREATED
        )

    @action(
        detail=True,
        methods=['post'],
        url_path='respond',
        url_name='respond'
    )
    def respond(self, request, pk=None):
        self.serializer_class = FrindsSerializerRes
        friendship = self.get_object()
        if friendship.to != request.user:
            return Response(
                {'error': 'Cannot respond to this request'},
                status=status.HTTP_403_FORBIDDEN
            )

        serializer = FrindsSerializerRes(data=request.data)
        if serializer.is_valid():
            serializer.update(friendship, serializer.validated_data)
            return Response(
                FreindsSerialiser(friendship).data,
                status=status.HTTP_200_OK
            )
        return Response(
            {'error': 'Bad request'},
            status=status.HTTP_400_BAD_REQUEST
        )

    @action(
        detail=False,
        methods=['get'],
        url_name='list-accepted',
        url_path='list-accepted'
    )
    def list_accepted(self, request):
        user = request.user
        friends = user.friends.all().order_by('name')
        return Response(
            UserSerilaizersForFriends(friends, many=True).data,
            status=status.HTTP_200_OK,
        )

    @action(
        detail=False, methods=['get'],
        url_name='list-pending',
        url_path='list-pending'
    )
    def list_pending(self, request):
        user = request.user

        pend_request = Friends.objects.filter(to=user, status='pending')
        return Response(
            FreindsSerialiser(pend_request, many=True).data,
            status=status.HTTP_200_OK
        )


class UserPagation(PageNumberPagination):
    page_size = 10


@extend_schema(
    parameters=[
        OpenApiParameter(
            name='search',
            description='serarch keyword',
            required='False',
            type=str
        )
    ]
)
class UserSerachViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = UserSerilaizersForFriends
    pagination_class = UserPagation
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def get_queryset(self):
        keyword = self.request.query_params.get('search', '')
        print(keyword)
        return models.User.objects.filter(
            Q(email__iexact=keyword) |
            Q(name__icontains=keyword)
        ).distinct().order_by('name')
