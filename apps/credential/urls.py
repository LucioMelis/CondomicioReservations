from django.urls import path
from apps.credential.views import CredentialsView

urlpatterns = [
    path('login/', CredentialsView.as_view(), name='login'),
    ]