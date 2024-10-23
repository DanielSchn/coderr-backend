from rest_framework import permissions

class IsOwnerOrAdmin(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        print(f'Object User: {obj.user}, Request User: {request.user}')
        if request.method in permissions.SAFE_METHODS:
            return bool(request.user and (request.user == obj.user or request.user.is_staff))
        if request.method == "PATCH":
            return bool(request.user and (request.user == obj.user or request.user.is_staff))

        return bool(request.user and (request.user == obj.user or request.user.is_staff))