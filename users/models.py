from django.db import models
from django.utils import timezone

# Create your models here.


class User(models.Model):
    class RoleEnum(models.TextChoices):
        ADMIN = 'Admin'
        USER = 'User'
    id = models.AutoField(primary_key=True)
    full_name = models.CharField(max_length=50)
    avatar = models.CharField(max_length=255, null=True)
    email = models.CharField(max_length=50)
    password = models.CharField(max_length=255)
    role = models.CharField(
        max_length=25, choices=RoleEnum.choices, default=RoleEnum.USER)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['created_at'])
        ]
