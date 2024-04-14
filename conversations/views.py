from django.shortcuts import render
from django.http import Http404, JsonResponse
from django.shortcuts import render
from pusher import Pusher
from rest_framework import views, status
from rest_framework.response import Response
from chatbot.helpers import custom_response, parse_request
from conversations.models import Conversation, Message, Participant
from conversations.serializers import ConversationSerializer, MessageSerializer
from users.models import User
from users.serializers import UserSerializer
import bcrypt
from rest_framework_simplejwt.tokens import RefreshToken
from django.core.exceptions import ObjectDoesNotExist
# Create your views here.

pusher = Pusher(app_id=u'1745392', key=u'ef136162ebafbc149f55',
                secret=u'3705ce1977b317f43be5', cluster=u'mt1')


class ConversationAPIView(views.APIView):
    def get(self, request):
        try:
            users = Conversation.objects.all()
            serializer = ConversationSerializer(users, many=True)
            return custom_response('Successfully!', 'Success', serializer.data, 200)
        except:
            return custom_response('Failed!', 'Error', None, 400)


class ConversationByUserAPIView(views.APIView):
    def get(self, request, user_id):
        try:
            participant_conversations = Participant.objects.filter(
                user_id=user_id)
            conversations_data = []

            for participant_conversation in participant_conversations:
                conversation = participant_conversation.conversation_id
                other_participant = Participant.objects.filter(
                    conversation_id=conversation).exclude(user_id=user_id).first()

                try:
                    last_message = Message.objects.filter(
                        conversation_id=conversation).latest('created_at')
                except ObjectDoesNotExist:
                    last_message = None
                other_user = {
                    'id': other_participant.user_id.id if other_participant else None,
                    'full_name': other_participant.user_id.full_name if other_participant else None,
                    'avatar': other_participant.user_id.avatar if other_participant else None,
                }
                conversation_data = {
                    'conversation_id': conversation.id,
                    'type': conversation.type,
                    'other_user': other_user,
                    'last_message_content': last_message.content if last_message else None,
                    'last_message_created_at': last_message.created_at.strftime('%Y-%m-%d %H:%M:%S') if last_message else None,
                }
                conversations_data.append(conversation_data)

            return custom_response('Successfully!', 'Success', conversations_data, 200)
        except Exception as e:
            return custom_response('Failed!', 'Error', str(e), 400)


class MessagesByConversationAPIView(views.APIView):
    def get(self, request, conversation_id):
        try:
            messages = Message.objects.filter(conversation_id=conversation_id)
            message_data = []
            for message in messages:
                message_info = {
                    'content': message.content,
                    'created_at': message.created_at,
                    'user_id': message.user_id.id,
                    'full_name': message.user_id.full_name,
                    'avatar': message.user_id.avatar,
                }
                message_data.append(message_info)
            return JsonResponse({'messages': message_data}, status=200)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

    def post(self, request, conversation_id):
        try:
            # Add the conversation_id to the message data before serializing
            message_data = request.data.copy()
            message_data['conversation_id'] = conversation_id

            serializer = MessageSerializer(data=message_data)
            if serializer.is_valid():
                serializer.save()
                # message = {'name': message.user.username, 'status': message.status,
                #            'message': message.message, 'id': message.id}
                pusher.trigger(u'my-channel', u'my-event', 'message')
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
