from django.urls import path, include

from .views import CreatePostView
from .views import PostWallView
from .views import PostDetailView
from .views import PostDeleteView
from .views import CommentCreateView

app_name = 'blog_system'

urlpatterns = [

    path('posts/', PostWallView.as_view(), name='posts_wall'),

    path('posts/create', CreatePostView.as_view(), name='create_post'),
    path('posts/<id>', PostDetailView.as_view(), name='post_detail'),

    path('posts/delete/<id>', PostDeleteView.as_view(), name='delete_post'),


    path('posts/<id>/comments/create', CommentCreateView.as_view(), name='create_comment'),

    # Api
    path('api/', include('blog_system.api.routers'))


]