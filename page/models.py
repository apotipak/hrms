from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
   language_code = models.CharField(max_length=2, blank=True, null=True)
   employee_id = models.CharField(max_length=10, blank=True, null=True)
   updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
