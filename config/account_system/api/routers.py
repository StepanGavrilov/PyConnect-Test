from django.urls import path, include

from .viewsets import GetUsersPublicView, AccountViewset, AccountCreateViewset, GetUsersPrivateView,\
    GetUsersFriendsPublicView, GetUsersFriendsPrivateView


urlpatterns = [
    # API

    # Информация о пользователе
    path('public/users/', GetUsersPublicView.as_view({
        'get': 'list',
    })),
    path('private/users/', GetUsersPrivateView.as_view({
        'get': 'list',
    })),
    path('public/users/<int:pk>', GetUsersPublicView.as_view({
        'get': 'retrieve',
    })),
    path('private/users/<int:pk>', GetUsersPrivateView.as_view({
        'get': 'retrieve',
    })),

    # Информация о друзьях пользоватедя
    path('public/users/friends/<int:pk>', GetUsersFriendsPublicView.as_view({
        'get': 'retrieve'
    })),
    path('private/users/friends/<int:pk>', GetUsersFriendsPrivateView.as_view({
        'get': 'retrieve',
    })),

    # User CRUD
    path('users/', AccountCreateViewset.as_view()),  # CREATE
    path('users/<id>', AccountViewset.as_view()),  # GET/DELETE/PATH/PUT


    # path('auth/', include('djoser.urls')),  # User
    path('auth/', include('djoser.urls.jwt')),  # Create/Update/Refresh JWTtoken
]