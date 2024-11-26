from rest_framework import permissions

from rest_framework.permissions import BasePermission


class IsOwner(permissions.BasePermission):
    """
    Разрешение для проверки, является ли пользователь владельцем объекта.
    """

    def has_object_permission(self, request, view, obj):
        # Предполагается, что у объекта есть поле `owner`
        return obj.owner == request.user


class IsModer(permissions.BasePermission):

    def has_permission(self, request, view):
         return request.user.groups.filter(name="moders").exists()
