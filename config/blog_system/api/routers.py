from django.urls import path, include

from .viewsets import PostViewset
from .viewsets import CommentAPIView

urlpatterns = [

    # CRUD POST
    path('posts/<id>', PostViewset.as_view({
        'get': 'retrieve',
        'delete': 'destroy',
        'put': 'update'
    })),  # GET
    path('posts/', PostViewset.as_view({
        'post': 'create',
        'get': 'list'
    })),  # CREATE / GET
    path('posts/<id>/comments/<comment_id>', CommentAPIView.as_view({
        'get': 'retrieve',
        'delete': 'destroy'
    })),


    path('posts/<id>/comments/', CommentAPIView.as_view({
        'get': 'list',
        'post': 'create',
    })),

]