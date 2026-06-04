from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import authenticate
from rest_framework import status
from oauth2_provider.models import Application, AccessToken, RefreshToken
from datetime import timedelta
from oauth2_provider.settings import oauth2_settings
from django.utils import timezone
import secrets

class CredentialsView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        username = request.data['username']
        password = request.data['password']

        user = authenticate(username=username, password=password)

        if not user:
            return Response(
                {'error': ''},
                status=status.HTTP_401_UNAUTHORIZED
            )

        try:
            app = Application.objects.get(name='default')
        except Application.DoesNotExist:
            return Response(
                {'error': 'OAuth application non configurata'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        AccessToken.objects.filter(user=user, application=app).delete()

        expire_seconds = oauth2_settings.ACCESS_TOKEN_EXPIRE_SECONDS
        access_token = AccessToken.objects.create(
            user=user,
            application=app,
            token=secrets.token_urlsafe(32),
            expires=timezone.now() + timedelta(seconds=expire_seconds),
            scope='read write',
        )

        refresh_token = RefreshToken.objects.create(
            user=user,
            application=app,
            token=secrets.token_urlsafe(32),
            access_token=access_token,
        )

        return Response({
            'access_token': access_token.token,
            'refresh_token': refresh_token.token,
            'token_type': 'Bearer',
            'expires_in': expire_seconds,
            'scope': access_token.scope,
        })