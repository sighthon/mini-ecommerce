from rest_framework import permissions

from user.models import User


class FinancialLedgerPermission(permissions.BasePermission):
    """
    The request is authenticated as a user, or is a read-only request.
    """

    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False

        if request.method == 'GET' and request.user.type not in [User.Types.SALES_AGENT, User.Types.ADMIN]:
            return False

        return True