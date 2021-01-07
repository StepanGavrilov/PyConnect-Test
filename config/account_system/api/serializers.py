from rest_framework import serializers

from friendship.models import Friend, Follow, Block, FriendshipRequest

from ..models import Account


class GetUsersPublicSerializer(serializers.ModelSerializer):
    """
    Выдаёт информацию об всех пользователях - Публичный
    """

    class Meta:
        model = Account
        fields = ('username', 'age', 'gender', 'first_name', 'last_name')


class GetUsersPrivateSerializer(serializers.ModelSerializer):
    """
    Выдаёт информацию об всех пользователях - Приватгый
    """

    class Meta:
        model = Account
        fields = ('username', 'age', 'gender', 'first_name', 'last_name', 'last_login', 'date_joined',
                  'is_staff')


class GetUserFriendsPublicSerializer(serializers.ModelSerializer):
    """
    Сериализатор, показывающий друзей и их модели - Публичный
    """
    to_user = GetUsersPublicSerializer(read_only=True)
    from_user = GetUsersPublicSerializer(read_only=True)

    class Meta:
        model = Friend
        fields = ('id', 'to_user', 'from_user')
        depth = 1


class GetUserFriendsPrivateSerializer(serializers.ModelSerializer):
    """
    Сериализатор, показывающий друзей и их модели - Приватный
    """
    to_user = GetUsersPrivateSerializer(read_only=True)
    from_user = GetUsersPrivateSerializer(read_only=True)

    class Meta:
        model = Friend
        fields = ('id', 'created', 'to_user', 'from_user')
        depth = 1