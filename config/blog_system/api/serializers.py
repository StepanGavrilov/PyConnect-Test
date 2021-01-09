from ..models import Post

from rest_framework import serializers


class PostCreateSerializer(serializers.ModelSerializer):
    """
    Серриализатор для постов
    """

    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Post
        fields = ('id', 'title', 'text', 'owner')
