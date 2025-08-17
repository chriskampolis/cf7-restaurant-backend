from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsManager(BasePermission):
    """User is authenticated and is a manager."""

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_manager()

class ReadOnlyOrIsManager(BasePermission):
    """
    Allow anyone to read (GET, HEAD, OPTIONS).
    Only managers can create/update/delete.
    """

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        return request.user.is_authenticated and request.user.is_manager()