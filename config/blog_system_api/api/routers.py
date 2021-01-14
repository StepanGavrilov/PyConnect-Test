from django.urls import path

from .viewsets import PostViewset, CommentAPIView


urlpatterns = [

    # CRUD POST
    path('posts/<id>', PostViewset.as_view({
        'get': 'retrieve',
        'delete': 'destroy',
        'put': 'update'
    })),  # GET
    path('posts/', PostViewset.as_view({
        'get': 'list',
        'post': 'create'
    })),  # CREATE / GET

    # CRUD COMMENT
    path('posts/<id>/comments/<comment_id>', CommentAPIView.as_view({
        'get': 'retrieve',
        'delete': 'destroy',
        'put': 'update'
    })),
    path('posts/<id>/comments/', CommentAPIView.as_view({
        'get': 'list',
        'post': 'create',
    })),

]