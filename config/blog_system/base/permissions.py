from rest_framework import permissions
from rest_framework.permissions import BasePermission


class IsAuthorEntry(BasePermission):
    """
    Проверяем автора объекта
    """
    def has_object_permission(self, request, view, obj):
        print('\nCheck 1\n')
        print(request)
        print(view)
        print(obj)
        return obj.owner == request.user or obj.entry.group.founder == request.user
