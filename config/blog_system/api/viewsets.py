from rest_framework import generics
from rest_framework import permissions
from rest_framework import mixins
from rest_framework import viewsets
from rest_framework import status

from rest_framework.response import Response

from .serializers import PostSerializer
from .serializers import PostCreateSerializer

from .serializers import CommentSerializer
from .serializers import CommentSerializerCreate

from ..models import Post
from ..models import Comment

from ..base.classes import CreateUpdateDestroy
from ..base.classes import ListRetrieveMixins

from ..base.permissions import IsAuthorEntry


class PostViewset(CreateUpdateDestroy, ListRetrieveMixins, viewsets.GenericViewSet):
    """
    CRUD Поста
    """
    permission_classes_by_action = {'delete': [IsAuthorEntry],
                                    }

    def get_permissions(self):
        print('\n\tPermissions\n')
        try:
            print('\tPermissions: ', self.permission_classes_by_action)
            # return permission_classes depending on `action`
            return [permission() for permission in self.permission_classes_by_action[self.action]]
        except KeyError:
            # action is not set return default permission_classes
            return [permission() for permission in self.permission_classes]

    def get_serializer_class(self):
        """
        Выбор сериализатора по дейсвтию пользователя
        """

        if self.action == 'create':
            print('\tCreate')
            return PostCreateSerializer
        elif self.action == 'list':
            print('\tList')
            return PostSerializer
        elif self.action == 'retrieve':
            print('\tRetrieve')
            return PostSerializer
        elif self.action == 'destroy':
            print('\tDestroy')
            return PostSerializer
        elif self.action == 'update':
            print('\tUpdate')
            return PostSerializer

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
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def perform_create(self, serializer) -> None:
        serializer.save(owner=self.request.user)

    # TODO CHECK PERMISSIONS
    def perform_destroy(self, instance):
        """
        """
        print('\n\tPerform destroy', instance)

    def destroy(self, request, *args, **kwargs):
        """
        """
        print('\n\n\tDestroy here\n\n')

        instance = self.get_object()
        print('\tPost object: ', instance, '\n\tRequest user: ', self.request.user)
        author_per = self.check_object_permissions(self.request, instance)
        print(f'\tAuthor permission: {author_per}')

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


class CommentAPIView(CreateUpdateDestroy, ListRetrieveMixins, viewsets.GenericViewSet):
    """
    CRUD Комментария
    """
    lookup_url_kwarg = 'id'
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_serializer_class(self):
        """
        Выбор сериализатора по дейсвтию пользователя
        """
        if self.action == 'list':
            return CommentSerializer
        elif self.action == 'create':
            return CommentSerializerCreate
        elif self.action == 'retrieve':
            return CommentSerializer

    def get_comment_detail(self) -> Comment:
        """
        Получение конкретного комметария
        """
        return Comment.objects.get(id=self.kwargs['comment_id'])

    def get_object(self) -> Post:
        """
        Получение поста, где находятся все его комментарии
        """
        return Post.objects.get(id=self.kwargs[self.lookup_url_kwarg])

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

    def destroy(self, request, *args, **kwargs):
        print('\t\nDestroy')
        pass
