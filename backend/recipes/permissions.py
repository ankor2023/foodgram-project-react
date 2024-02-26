from rest_framework import permissions

class IsOwnerOrReadOnly(permissions.IsAuthenticatedOrReadOnly):
    """Anonymous user can read.
    Authenticated user can create.
    Owner or Admin can change.
    """

    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS
            or (request.user.is_authenticated and request.user.is_superuser)
            or obj.author == request.user
        )

