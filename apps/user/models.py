from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

class User(AbstractUser):
    phone_number = models.CharField(unique=True, max_length=20, verbose_name=_('phone number'))
    address = models.CharField(max_length=100, verbose_name=_('address'))
    city = models.CharField(max_length=100, verbose_name=_('city'))
    zip_code = models.CharField(max_length=20, verbose_name=_('zip_code'))
    country = models.CharField(max_length=100, verbose_name=_('country'))
    deleted = models.BooleanField(default=False, verbose_name=_('deleted'))

