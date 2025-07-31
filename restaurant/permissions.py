from rest_framework import permissions

class IsManager(permissions.BasePermission):
    """Only managers have full access."""

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_manager()

class IsManagerOrReadOnlyMenuItem(permissions.BasePermission):
    """Managers can CRUD MenuItems; employees can only read."""

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return request.user.is_authenticated
        return request.user.is_authenticated and request.user.is_manager()