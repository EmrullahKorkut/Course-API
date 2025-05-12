from rest_framework import permissions

class IsAdminOrReadOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return request.user and request.user.is_authenticated
        
        return request.user.is_superuser
    


class IsAdminOrTeacherOrReadOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        
        if not request.user.is_authenticated:
            return False
        
        if request.user.is_superuser:
            return True
        
        if request.user.is_teacher:
            return True

        return False

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        
        if not request.user.is_authenticated:
            return False
        
        if request.user.is_superuser:
            return True
        
        if obj.teacher == request.user:
            return True

        return False



class IsStudentOrReadOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
           return True
        if request.user.is_student:
            return True
        return False
    



# class IsCardOwner(permissions.BasePermission):

#     def has_permission(self, request, view):
        
#         if request.method in permissions.SAFE_METHODS:
#             return True
        
#         if request.user.is_authenticated and request.user.is_student == True:
#             return True
        
#         if request.user.is_superuser == True or request.user.is_teacher == True:
#             return False


class IsReviewOwnerOrAdminOrReadOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        pass
    

    def has_object_permission(self, request, view, obj):
        pass
    
