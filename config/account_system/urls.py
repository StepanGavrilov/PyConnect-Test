from django.urls import path, include

from .views import get_user_edit, get_make_friendship, get_delete_friendship, PublicAccountView, add_friend,\
    AccountProfileView, AccountRegisterView, UserLogOutView, AccountFriends, AccountLoginView, SearchFriendsView,\
    AccountChangePasswordView


app_name = 'account_system'

urlpatterns = [

    # Account
    path('login', AccountLoginView.as_view(), name='login'),
    path('logout', UserLogOutView.as_view(), name='logout'),
    path('register', AccountRegisterView.as_view(), name='register'),
    path('me/', AccountProfileView.as_view(), name='profile'),

    path('me/edit/password', AccountChangePasswordView.as_view(), name='change_password'),
    path('me/edit', get_user_edit, name='edit_accounts'),

    path('friends/', AccountFriends.as_view(), name='friends'),
    path('friends/search', SearchFriendsView.as_view(), name='search_friends'),
    path('friends/add/<master_account_id>', add_friend, name='add_friend'),
    path('friends/add/friend/<slave_user_id>', get_make_friendship, name='get_make_friendship'),
    path('friends/delete/<slave_user_id>', get_delete_friendship, name='get_delete_friendship'),

    path('user/<id>', PublicAccountView.as_view(), name='public_profile'),


    # Apps
    path('friendship/', include('friendship.urls')),
    # SocialAuth
]