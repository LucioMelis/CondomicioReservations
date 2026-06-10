from apps.api.exceptions import APIValidationException
from apps.api.permissions import ApiIsAuthenticatedAsAdminPermission
from rest_framework.viewsets import ModelViewSet
from django.http.response import HttpResponse
from apps.user.serializers import UserSerializer


class UserListView(ModelViewSet):
    permission_classes = (ApiIsAuthenticatedAsAdminPermission,)
    serializer_class = UserSerializer
    def create(self,request,*args,**kwargs):
        name = request.data.get("name")
        response = HttpResponse("Hello, Henry you have a shit connection Man!")
        if not name:
            raise APIValidationException("No name provided","error_name_attribute")
        return response