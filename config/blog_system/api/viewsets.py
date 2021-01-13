from rest_framework import generics, permissions, mixins, viewsets, status
from rest_framework.generics import RetrieveUpdateDestroyAPIView

from rest_framework.response import Response


from .serializers import PostSerializer
from .serializers import CommentSerializer
from .serializers import CommentSerializerCreate

from ..models import Post
from ..models import Comment

from ..base.permissions import IsAuthorEntry

from ..base.classes import CreateUpdateDestroy
from ..base.classes import ListRetrieveMixins


class PostViewset(mixins.CreateModelMixin,
                  mixins.RetrieveModelMixin,
                  mixins.ListModelMixin,
                  mixins.DestroyModelMixin,
                  mixins.UpdateModelMixin,
                  viewsets.GenericViewSet):
    """
    CRUD Поста
    """

    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    serializer_class = PostSerializer

    # permission_classes_by_action = {'get': [permissions.AllowAny],
    #                                 'post': [permissions.IsAuthenticated],
    #                                 'put': [IsAuthorEntry],
    #                                 'delete': [IsAuthorEntry],
    #                                 }

    def get_queryset(self):
        return Post.objects.all()

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        post = serializer.save()
        return Response({'post': PostSerializer(post, context=self.get_serializer_context()).data})

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class CommentAPIView(CreateUpdateDestroy, ListRetrieveMixins, viewsets.GenericViewSet):
    """
    CRUD Комментария
    """
    serializer_class = CommentSerializer
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
        Получение кокнретного комметария
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

    def retrieve(self, request, *args, **kwargs):
        """
        """
        instance = self.get_comment_detail()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        print('\t\nDestroy')
        pass