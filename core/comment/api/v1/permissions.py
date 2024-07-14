from rest_framework.permissions import BasePermission


class IsOwnerOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        return True

    def has_object_permission(self, request, view, obj):
        return obj.author.user == request.user
