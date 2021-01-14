from rest_framework import viewsets, status

from rest_framework.response import Response

from .serializers import PostSerializer, PostCreateSerializer

from .serializers import CommentSerializer, CommentSerializerCreate

from blog_system.models import Post, Comment

from ..base.classes import CreateUpdateDestroy, ListRetrieveMixins

from ..base.permissions import IsAuthorEntry, IsAuthorCommentEntry


class PostViewset(CreateUpdateDestroy, ListRetrieveMixins, viewsets.GenericViewSet):
    """
    CRUD Поста
    """

    permission_classes = (IsAuthorEntry,)

    def get_serializer_class(self):
        """
        Выбор сериализатора по дейсвтию пользователя
        """

        if self.action == 'create':
            return PostCreateSerializer
        elif self.action == 'list':
            return PostSerializer
        elif self.action == 'retrieve':
            return PostSerializer
        elif self.action == 'destroy':
            return PostSerializer
        elif self.action == 'update':
            return PostCreateSerializer

    def get_object(self):
        """
        Получение конкретного поста
        """
        try:
            post = Post.objects.get(id=self.kwargs['id'])
        except Post.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        return post

    def get_queryset(self) -> Post:
        return Post.objects.all()

    def retrieve(self, request, *args, **kwargs) -> Response:
        """
        Развёрнутый пост
        """
        instance = self.get_object()
        if isinstance(instance, Post):
            serializer = self.get_serializer(instance)
            return Response(serializer.data)
        return Response(status=status.HTTP_404_NOT_FOUND)

    def perform_create(self, serializer) -> None:
        serializer.save(owner=self.request.user)

    def perform_destroy(self, instance) -> None:
        """
        """
        instance.delete()

    def destroy(self, request, *args, **kwargs) -> Response:
        """
        """
        instance = self.get_object()
        if not isinstance(instance, Post):
            return Response(status=status.HTTP_404_NOT_FOUND)
        self.check_object_permissions(self.request, instance)
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def create(self, request, *args, **kwargs) -> Response:
        """
        Создание поста
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        post = serializer
        return Response({'post': post.data})

    def partial_update(self, request, *args, **kwargs) -> Response:
        """
        """
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)

    def update(self, request, *args, **kwargs) -> Response:
        """
        """
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        if not isinstance(instance, Post):
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.check_object_permissions(self.request, instance)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)


class CommentAPIView(CreateUpdateDestroy, ListRetrieveMixins, viewsets.GenericViewSet):
    """
    CRUD Комментария
    """
    lookup_url_kwarg = 'id'
    permission_classes = (IsAuthorCommentEntry,)

    def get_serializer_class(self):
        """
        Выбор сериализатора по дейсвтию пользователя
        """

        if self.action == 'create':
            return CommentSerializerCreate
        elif self.action == 'list':
            return CommentSerializer
        elif self.action == 'retrieve':
            return CommentSerializer
        elif self.action == 'destroy':
            return CommentSerializer
        elif self.action == 'update':
            return CommentSerializerCreate

    def get_comment_detail(self):
        """
        Получение конкретного комметария
        """
        try:
            comment = Comment.objects.get(id=self.kwargs['comment_id'])
        except Comment.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        return comment

    def get_object(self):
        """
        Получение поста, где находятся все его комментарии
        """
        try:
            post = Post.objects.get(id=self.kwargs[self.lookup_url_kwarg])
        except Post.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        return post

    def get_queryset(self) -> Comment:
        """
        Получение всех комментраиев конкретного поста
        """
        return Comment.objects.select_related().filter(post=self.kwargs[self.lookup_url_kwarg])

    def perform_create(self, serializer):
        serializer.save(post=self.get_object(), author=self.request.user)

    def create(self, request, *args, **kwargs) -> Response:
        """
        Создаёт комментарий к посту ( id поста из URL )
        """
        serialize_class = self.get_serializer_class()
        serializer = serialize_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        comment = serializer
        return Response({'comment': comment.data})

    def retrieve(self, request, *args, **kwargs) -> Response:
        """
        Развёрнутый комментарий
        """
        instance = self.get_comment_detail()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def perform_destroy(self, instance) -> None:
        instance.delete()

    def destroy(self, request, *args, **kwargs) -> Response:

        instance = self.get_comment_detail()  # Post
        if not isinstance(instance, Comment):
            return Response(status=status.HTTP_404_NOT_FOUND)

        self.check_object_permissions(self.request, instance)
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def partial_update(self, request, *args, **kwargs) -> Response:
        """
        """
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)

    def update(self, request, *args, **kwargs) -> Response:
        """
        """
        partial = kwargs.pop('partial', False)
        instance = self.get_comment_detail()
        if not isinstance(instance, Comment):
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.check_object_permissions(self.request, instance)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)