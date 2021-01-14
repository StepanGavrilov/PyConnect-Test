
from rest_framework import serializers

from blog_system.models import Post, Comment


class PostSerializer(serializers.ModelSerializer):
    """
    Серриализатор для постов
    """

    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Post
        fields = ('id', 'title', 'text', 'owner')


class PostCreateSerializer(serializers.ModelSerializer):
    """
    Серриализатор для создания постов
    """

    class Meta:
        model = Post
        fields = ('title', 'text')

    def create(self, validated_data):
        post = Post.objects.create(**validated_data)
        return post

    def update(self, instance, validated_data):
        for (key, value) in validated_data.items():
            setattr(instance, key, value)
        instance.save()
        return instance


class CommentSerializer(serializers.ModelSerializer):
    """
    Сериализатор для комментариев под постами
    """

    post = PostSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = ('id', 'post', 'created', 'author', 'text')


class CommentSerializerCreate(serializers.ModelSerializer):
    """
    Серриализатор для создания комментариев под постами
    """

    class Meta:
        model = Comment
        fields = ('text', )

    def create(self, validated_data):
        comment = Comment.objects.create(**validated_data)
        return comment

    def update(self, instance, validated_data):
        for (key, value) in validated_data.items():
            setattr(instance, key, value)
        instance.save()
        return instance