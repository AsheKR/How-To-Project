from rest_framework import permissions


class IsOwnerorReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in ['GET', 'OPTIONS', 'HEAD']:
            return True
        else:
            return bool(
                request.user and
                request.user.is_authenticated and
                request.user == obj
            )
