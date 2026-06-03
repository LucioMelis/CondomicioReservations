from rest_framework.permissions import IsAuthenticated

class ApiIsAuthenticatedPermission(IsAuthenticated):
    pass

class ApiIsAuthenticatedAsAdminPermission(ApiIsAuthenticatedPermission):
    def has_permission(self, request, view):
        permission = super(ApiIsAuthenticatedAsAdminPermission,self).has_permission(request, view)
        if not permission:
            return permission
        user = request.user
        return permission and user.groups.filter(name='Admin').exists()

class ApiIsAuthenticatedAsCustomerPermission(ApiIsAuthenticatedPermission):
    def has_permission(self, request, view):
        permission = super(ApiIsAuthenticatedAsCustomerPermission,self).has_permission(request, view)
        if not permission:
            return permission
        user = request.user
        return permission and user.groups.filter(name='Customer').exists()

class ApiReadAllowAnyCreateAdminPermission(ApiIsAuthenticatedPermission):
    def has_permission(self, request, view):
        permission = super(ApiReadAllowAnyCreateAdminPermission, self).has_permission(request, view)
        if not permission:
            return permission
        user = request.user

        if request.method == 'GET':
            return permission

        else:
            return permission and user.groups.filter(name='Admin').exists()

class ApiReadAllowAnyCreateCustomerPermission(ApiIsAuthenticatedPermission):
    def has_permission(self, request, view):
        permission = super(ApiReadAllowAnyCreateCustomerPermission, self).has_permission(request, view)
        if not permission:
            return permission
        user = request.user

        if request.method == 'GET':
            return permission

        else:
            return permission and user.groups.filter(name="Customer").exists()

