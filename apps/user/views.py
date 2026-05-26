from rest_framework.permissions import AllowAny
from rest_framework.viewsets import ModelViewSet
from django.http.response import HttpResponse


class UserListView(ModelViewSet):
    permission_classes = [AllowAny]
    def create(self,request,*args,**kwargs):
        response = HttpResponse("Hello, Henry you have a shit connection Man!")
        return response