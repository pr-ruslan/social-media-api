from rest_framework import permissions

class IsAdminOrIsSelf(permissions.BasePermission):
    """
    Custom permission to only allow admins or the owner of the profile to edit/view it.
    """
    def has_object_permission(self, request, view, obj):
        # 1. Allow if the user is an admin/staff
        if request.user and request.user.is_staff:
            return True

        # 2. Allow if the object being accessed belongs to the current user
        # 'obj' is the Profile instance, so we check obj.user
        return obj.user == request.user