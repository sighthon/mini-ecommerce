from rest_framework import permissions

from user.models import User


class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.type == User.Types.ADMIN
