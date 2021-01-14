from django.urls import path, include

from .views import CreatePostView, PostWallView, PostDetailView, PostDeleteView, CommentCreateView


app_name = 'blog_system'

urlpatterns = [

    path('posts/', PostWallView.as_view(), name='posts_wall'),

    path('posts/create', CreatePostView.as_view(), name='create_post'),
    path('posts/<id>', PostDetailView.as_view(), name='post_detail'),

    path('posts/delete/<id>', PostDeleteView.as_view(), name='delete_post'),


    path('posts/<id>/comments/create', CommentCreateView.as_view(), name='create_comment'),


]