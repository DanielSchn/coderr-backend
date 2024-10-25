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
        print(f'Request User: {request.user} {request.user.is_staff}')
        if request.method in permissions.SAFE_METHODS:
            return True
        
        elif request.method in ['POST', 'PUT', 'PATCH', 'DELETE']:
            if request.user.is_staff:
                return True
            else: 
                user_profile = getattr(request.user, 'user_profile', None)
                if user_profile.type == 'business':
                    return True
            
            return False
        
        return False
    

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        
        elif request.method in ['POST', 'PUT', 'PATCH', 'DELETE']:
            if request.user.is_staff:
                return True
            else: 
                user_profile = getattr(request.user, 'user_profile', None)
                if user_profile.type == 'business':
                    return True
            
            return False
        
        return False
        
        