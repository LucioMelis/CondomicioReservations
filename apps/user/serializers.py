from django.contrib.auth import get_user_model
from apps.api.custom_serializers import BaseModelSerializer
from rest_framework import serializers


class UserSerializer(BaseModelSerializer):
    user_type = serializers.SerializerMethodField()
    full_name = serializers.SerializerMethodField()

    class Meta:
        model = get_user_model()
        fields = ('id', 'first_name', 'last_name', 'email', 'full_name', 'city', 'phone_number', 'country',
                  'address','zip_code','deleted','user_type')

    def get_full_name(self, obj):
        return obj.get_full_name()

    def get_user_type(self, obj):
        return f'{obj.groups.first()}'
