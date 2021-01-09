from rest_framework import generics, permissions, mixins, viewsets
from rest_framework.response import Response

from .serializers import PostCreateSerializer

from ..models import Post

from ..base.permissions import IsAuthorEntry


class PostCreateViewset(mixins.CreateModelMixin,
                        mixins.RetrieveModelMixin,
                        mixins.ListModelMixin,
                        mixins.DestroyModelMixin,
                        mixins.UpdateModelMixin,
                        viewsets.GenericViewSet):
    """
    CRUD для поста с permission access
    """

    permission_classes = [permissions.IsAuthenticated]
    serializer_class = PostCreateSerializer
    queryset = Post.objects.all()
    permission_classes_by_action = {'get': [permissions.AllowAny],
                                    'post': [permissions.IsAuthenticated],
                                    'put': [IsAuthorEntry],
                                    'delete': [IsAuthorEntry],
                                    }

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        post = serializer.save()
        return Response({'post': PostCreateSerializer(post, context=self.get_serializer_context()).data})

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)