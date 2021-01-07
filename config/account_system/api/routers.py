from django.urls import path, include

from .viewsets import GetUsersPublicView
from .viewsets import GetUsersPrivateView
from .viewsets import GetUsersFriendsPublicView
from .viewsets import GetUsersFriendsPrivateView


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



    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
]