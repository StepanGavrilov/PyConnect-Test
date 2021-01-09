import rest_framework
from django.http import Http404
from rest_framework import permissions, views, status
from rest_framework import generics
from rest_framework.permissions import DjangoModelPermissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from friendship.models import Friend, Follow, Block, FriendshipRequest

from .serializers import GetUsersPrivateSerializer, AccountSerializer, AccountCreateSerializer
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


class AccountViewset(APIView):
    """
    Аккаунт пользователя CRUD
    """

    serializer_class = AccountSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_account(self, account_id):
        """
        Возвращаем акканут пользователя по id
        """
        try:
            return Account.objects.get(id=account_id)
        except Account.DoesNotExist:
            return None

    def get(self, request, **kwargs):
        """
        Вывод инфомрации о аккануте по id
        """
        account = self.get_account(kwargs['id'])
        if account is not None:
            serializer = AccountSerializer(account)
            return Response(serializer.data)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def delete(self, request, **kwargs):
        """
        Удаление аккаунта по id
        """
        account = self.get_account(kwargs['id'])
        if account is not None:
            """
            Если get_object вернул не None
            """
            if self.request.user.id == account.id:
                """
                Провека подлинности пользователя
                """
                account.delete()
                return Response(status=status.HTTP_200_OK)
            return Response(status=status.HTTP_403_FORBIDDEN)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def patch(self, request, **kwargs):
        """
        Обовление уже заполненных (только!) данных
        """
        account = self.get_account(kwargs['id'])
        if account is not None:
            if self.request.user.id == account.id:
                serializer = self.serializer_class(request.user, data=request.data, partial=True)
                serializer.is_valid(raise_exception=True)
                serializer.save()
                return Response({'Updated': serializer.data})
            return Response(status=status.HTTP_403_FORBIDDEN)
        return Response(status=status.HTTP_204_NO_CONTENT)


class AccountCreateViewset(generics.CreateAPIView):
    """
    Создания аккаунта пользователя
    """

    serializer_class = AccountCreateSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        account = serializer.save()
        return Response({'account': AccountCreateSerializer(account, context=self.get_serializer_context()).data})
