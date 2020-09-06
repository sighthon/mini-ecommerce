from rest_framework import permissions

from user.models import User


class ProductPermission(permissions.BasePermission):
    """
    The request is authenticated as a user, or is a read-only request.
    """
    SAFE_METHODS = ['GET', 'HEAD', 'OPTIONS']

    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        if request.method not in self.SAFE_METHODS and request.user.type != User.Types.ADMIN:
            return False
        return True
