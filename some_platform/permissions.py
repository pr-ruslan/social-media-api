from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsAdminOrSelfOrReadOnly(BasePermission):
    """
    Object-level permission:
    - Admins have full access
    - Users can act on their own object
    - Read-only requests are allowed for everyone
    """
    def has_object_permission(self, request, view, obj):
        # Always allow safe methods
        if request.method in SAFE_METHODS:
            return True

        # Admins can do anything
        if request.user.is_staff or request.user.is_superuser:
            return True

        # Normal user can act only on their own object
        # For UserProfile, obj.user is the owner
        return hasattr(obj, "user") and obj.user == request.user
