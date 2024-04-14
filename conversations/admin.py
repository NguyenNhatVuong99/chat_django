from django.contrib import admin

from conversations.models import Conversation, Participant, Message

# Register your models here.
admin.site.register(Conversation)
admin.site.register(Participant)
admin.site.register(Message)
