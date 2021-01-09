from django.urls import path, include

from .viewsets import PostCreateViewset

urlpatterns = [

    # CRUD POST

    path('posts/', PostCreateViewset.as_view({'post': 'create', 'get': 'list'})),  # CREATE / GET
    path('posts/<pk>', PostCreateViewset.as_view({'get': 'retrieve', 'delete': 'destroy', 'put': 'update'})),  # GET retrieve post
    # path('posts/<id>')  # GET/UPDATE/DELETE

]