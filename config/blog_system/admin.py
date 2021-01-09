from django.contrib import admin

from .models import Post


@admin.register(Post)
class AdminPost(admin.ModelAdmin):
    """
    Пост пользователя
    """
    list_display = ('id', 'owner', 'created', 'last_update')