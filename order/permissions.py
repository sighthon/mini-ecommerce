from rest_framework import permissions

from user.models import User


class OrderPermission(permissions.BasePermission):
    """
    The request is authenticated as a user, or is a read-only request.
    """

    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False

        # Only customer is allowed to place an order
        if request.method == 'POST' and request.user.type != User.Types.CUSTOMER:
            return False

        # Only Sales Agent is allowed to update an order
        if request.method == 'PATCH' and request.user.type != User.Types.SALES_AGENT:
            return False

        return True
