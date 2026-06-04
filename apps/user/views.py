from apps.api.permissions import ApiIsAuthenticatedAsAdminPermission
from rest_framework.viewsets import ModelViewSet
from django.http.response import HttpResponse
from apps.api.exceptions import APIBaseException

class UserListView(ModelViewSet):
    permission_classes = (ApiIsAuthenticatedAsAdminPermission,)
    def create(self,request,*args,**kwargs):
        name = request.get("name")
        if not name:
            raise APIBaseException("name is required", request.user)

        response = HttpResponse("Hello, Henry you have a shit connection Man!")
        return response