from rest_framework import permissions


class IsAuthorOrReadOnly(permissions.BasePermission):
    """
        Use this permission to restrict write access to a reservation author.
    """
    def has_object_permission(self, request, view, obj):
        # Read-only permissions are allowed for any request
        if request.method in permissions.SAFE_METHODS:
            return True
        # Write permissions are only allowed to the author of a reservation
        return obj.author == request.user
