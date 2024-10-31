from rest_framework import permissions

class IsObjectOwnerOrAdminPermission(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return bool(request.user and (request.user == obj.user or request.user.is_staff))
        
        if request.method == "PATCH":
            return bool(request.user and (request.user == obj.user or request.user.is_staff))

        return bool(request.user and (request.user == obj.user or request.user.is_staff))
    

class IsBusinessOrAdminPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        
        elif request.method in ['POST', 'PUT', 'PATCH', 'DELETE']:
            if request.user.is_staff:
                return True
            else: 
                if request.user.user_profile.type == 'business':
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
                
                if request.user.user_profile.type == 'business':
                    return True
            
            return False
        
        return False
        

class IsCustomerReadOnlyPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        
        if request.method in permissions.SAFE_METHODS:
            return True
        
        if request.user.user_profile.type == 'customer':
            return False
            
        return False
    

class OrderAccessPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        
        if request.method in permissions.SAFE_METHODS:
            return True
        
        if request.user.is_staff:
            return request.method != 'POST'
        
        if request.user.user_profile.type == 'customer':
                return request.method == 'POST'
        
        if request.user.user_profile.type == 'business':
                return request.method == 'PATCH'
        
        return False
    

class IsReviewerOrAdminPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        
        if request.user.is_staff:
            return request.method != 'POST'

        if request.method == 'POST':
            return request.user.user_profile.type == 'customer'
        
        if request.method in ['PATCH', 'DELETE']:
            return True
        
        return True
    
    def has_object_permission(self, request, view, obj):
        if request.method in ['PATCH', 'DELETE']:
            return obj.customer_user == request.user or request.user.is_staff
        
        return True