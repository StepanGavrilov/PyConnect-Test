from ..models import Post
from ..models import Comment

from rest_framework import serializers


class PostSerializer(serializers.ModelSerializer):
    """
    Серриализатор для постов
    """

    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Post
        fields = ('id', 'title', 'text', 'owner')


class CommentSerializer(serializers.ModelSerializer):
    """
    Сериализатор для комментариев под постами
    """

    post = PostSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = ('id', 'post', 'created', 'author', 'text')


class CommentSerializerCreate(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = ('text', )

    def create(self, validated_data):
        comment = Comment.objects.create(**validated_data)
        return comment