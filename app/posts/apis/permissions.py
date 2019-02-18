from rest_framework.permissions import BasePermission


class PostUpdateDestroyMustBeOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method == 'GET':
            return True
        elif request.method in ['PATCH', 'DELETE']:
            if request.user.is_authenticated and obj.author == request.user:
                return True

        return False
