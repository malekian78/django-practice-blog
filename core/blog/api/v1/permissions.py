from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsOwnerOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.user:
            return True
        else:
            return False

    def has_object_permission(self, request, view, obj):
        if obj.author.user == request.user:
            return True
        else:
            return False
