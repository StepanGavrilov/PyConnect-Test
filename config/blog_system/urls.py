from django.urls import path, include

from .views import CreatePostView
from .views import PostWallView

app_name = 'blog_system'

urlpatterns = [

    path('posts/create', CreatePostView.as_view(), name='create_post'),
    path('posts/', PostWallView.as_view(), name='posts_wall'),

    # Api
    path('api/', include('blog_system.api.routers'))


]