from django.urls import path, include

app_name = 'blog_system_api'

urlpatterns = [

    path('', include('blog_system_api.api.routers'))

]
