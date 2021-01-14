from django.contrib import admin

from .models import Post, Comment


@admin.register(Post)
class AdminPost(admin.ModelAdmin):
    """
    Пост пользователя
    """
    list_display = ('id', 'owner', 'created', 'last_update')


@admin.register(Comment)
class AdminComment(admin.ModelAdmin):
    """
    Коммент к посту
    """
    list_display = ('id', 'post', 'author', 'created')