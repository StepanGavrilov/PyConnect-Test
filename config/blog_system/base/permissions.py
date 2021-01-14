from rest_framework.permissions import BasePermission


class IsAuthorEntry(BasePermission):
    """
    Проверяем автора объекта
    """
    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user


class IsAuthorCommentEntry(BasePermission):
    """
    Проверяем автора объекта
    """
    def has_object_permission(self, request, view, obj):
        return obj.author == request.user
