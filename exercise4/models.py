from django.conf import settings
from django.db import models
from django.utils import timezone
from django.core.validators import RegexValidator

class Contact(
        models.Model):
    numOnly = RegexValidator(r'^\d*$', 'Please Input you Contact Number.')
    creator = models.ForeignKey(
            settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    FirstName = models.CharField(
            max_length=200)
    LastName = models.CharField(
            max_length=200)
    ContactNo = models.CharField(
            max_length=200,validators=[numOnly])
    Address = models.CharField(
            max_length=200)