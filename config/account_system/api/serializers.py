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


class AccountSerializer(serializers.ModelSerializer):
    """
    Сериализатор для акканута пользователя
    """

    class Meta:
        model = Account
        fields = ('id', 'username', 'first_name', 'last_name',
                  'about_me')

    def update(self, instance, validated_data):
        for (key, value) in validated_data.items():
            setattr(instance, key, value)
        instance.save()
        return instance


class AccountCreateSerializer(serializers.ModelSerializer):
    """
    Сериализатор создания акканута пользователя
    """

    class Meta:
        model = Account
        fields = ('id', 'username', 'email', 'password')

    def create(self, validated_data):
        account = Account.objects.create_user(**validated_data)
        return account
