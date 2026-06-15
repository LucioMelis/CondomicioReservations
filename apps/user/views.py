from apps.api.exceptions import APIValidationException
from apps.api.permissions import ApiIsAuthenticatedAsAdminPermission
from rest_framework.viewsets import ModelViewSet
from django.http.response import HttpResponse
from apps.user.serializers import UserSerializer
from apps.api.errors import APIErrorExtender

class UserListView(ModelViewSet):
    permission_classes = (ApiIsAuthenticatedAsAdminPermission,)
    serializer_class = UserSerializer

    def create(self,request,*args,**kwargs):
        name = request.data.get("name")
        response = HttpResponse("Hello, Henry you have a shit connection Man!")
        if not name:
            raise APIValidationException("No name provided",APIErrorExtender.missing_username)

        email = request.data.get("email")
        response = HttpResponse("Hello, Henry you have a shit connection Man!")
        if not name:
            raise APIValidationException("No email provided", APIErrorExtender.missing_email)
        return response