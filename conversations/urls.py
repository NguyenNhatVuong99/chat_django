from conversations import views
from django.urls import path

urlpatterns = [
    path('conversations', views.ConversationAPIView.as_view()),
    path('conversations/<int:user_id>',
         views.ConversationByUserAPIView.as_view(), name="get conversation"),
    path('conversations/<int:conversation_id>/messages',
         views.MessagesByConversationAPIView.as_view()),
]
