from django.db import models
from django.utils import timezone
from users.models import User

# Create your models here.


class Conversation(models.Model):
    class TypeConversationEnum(models.TextChoices):
        GROUP = 'Group'
        CUPPLE = 'Cupple'
    id = models.AutoField(primary_key=True)
    type = models.CharField(
        max_length=25, choices=TypeConversationEnum.choices, default=TypeConversationEnum.CUPPLE)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)


class Participant(models.Model):
    id = models.AutoField(primary_key=True)
    conversation_id = models.ForeignKey(
        Conversation, on_delete=models.CASCADE, related_name='conversation', null=False)
    user_id = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='participant', null=False)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)


class Message(models.Model):
    class TypeMessageEnum(models.TextChoices):
        TEXT = 'Text'
        FILE = 'File'
    id = models.AutoField(primary_key=True)
    conversation_id = models.ForeignKey(
        Conversation, on_delete=models.CASCADE, related_name='message', null=False)
    user_id = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='message', null=False)
    type = models.CharField(
        max_length=25, choices=TypeMessageEnum.choices, default=TypeMessageEnum.TEXT)
    content = models.TextField(max_length=255)
    is_read = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
