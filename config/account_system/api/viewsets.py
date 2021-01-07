from rest_framework import permissions
from rest_framework.viewsets import ModelViewSet

from friendship.models import Friend, Follow, Block, FriendshipRequest


from .serializers import GetUsersPrivateSerializer
from .serializers import GetUsersPublicSerializer
from .serializers import GetUserFriendsPrivateSerializer
from .serializers import GetUserFriendsPublicSerializer

from ..models import Account


class GetUsersPrivateView(ModelViewSet):
    """
    Информация о пользователе - приватная
    """
    serializer_class = GetUsersPrivateSerializer
    queryset = Account.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Account.objects.filter(id=self.request.user.id)


class GetUsersPublicView(ModelViewSet):
    """
    Информация о пользователе - публичная
    """
    serializer_class = GetUsersPublicSerializer
    queryset = Account.objects.all()
    permission_classes = [permissions.AllowAny]


class GetUsersFriendsPublicView(ModelViewSet):
    """
    Информация о друзья пользователя - публичная
    """
    serializer_class = GetUserFriendsPublicSerializer
    queryset = Friend.objects.all()
    permission_classes = [permissions.AllowAny]


class GetUsersFriendsPrivateView(ModelViewSet):
    """
    Информация о друзья пользователя - приватная
    """
    serializer_class = GetUserFriendsPrivateSerializer
    queryset = Friend.objects.all()
    permission_classes = [permissions.IsAuthenticated]
