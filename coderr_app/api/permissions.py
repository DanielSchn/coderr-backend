from rest_framework import permissions

class IsOwnerOrAdmin(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        print(f'Object User: {obj.user}, Request User: {request.user}')
        if request.method in permissions.SAFE_METHODS:
            return bool(request.user and (request.user == obj.user or request.user.is_staff))
        
        if request.method == "PATCH":
            return bool(request.user and (request.user == obj.user or request.user.is_staff))

        return bool(request.user and (request.user == obj.user or request.user.is_staff))
    

class IsBusinessUserOrAdmin(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        
        elif request.method in ['POST', 'PUT', 'PATCH', 'DELETE']:
            user_profile = getattr(request.user, 'user_profile', None)
            return user_profile and (user_profile.type == 'business' or request.user.is_staff)
        
        return False
    
    
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        
        elif request.method in ['POST', 'PUT', 'PATCH', 'DELETE']:
            user_profile = getattr(request.user, 'user_profile', None)
            return user_profile and (user_profile.type == 'business' or request.user.is_staff)
        
        return False
        
        