from django.http import Http404
from django.shortcuts import render
from rest_framework import views, status
from rest_framework.response import Response
from chatbot.helpers import custom_response, parse_request
from users.models import User
import bcrypt
from rest_framework_simplejwt.tokens import RefreshToken

from users.serializers import UserSerializer

# Create your views here.


class UserAPIView(views.APIView):
    def get(self, request):
        try:
            users = User.objects.all()
            serializer = UserSerializer(users, many=True)
            return custom_response('Successfully!', 'Success', serializer.data, 200)
        except:
            return custom_response('Failed!', 'Error', None, 400)

    def get_by_id(self, id):
        print(id)

    def post(self, request):
        data = parse_request(request)
        hashed_password = bcrypt.hashpw(
            data['password'].encode('utf-8'), bcrypt.gensalt())
        data['password'] = hashed_password.decode('utf-8')
        serializer = UserSerializer(data=data)

        if serializer.is_valid():
            serializer.save()
            return custom_response('Successfully!', 'Success', serializer.data, 201)
        else:
            return custom_response('Failed!', 'Error', serializer.errors, 400)


class UserDetailAPIView(views.APIView):
    def get_object(self, id_slug):
        try:
            return User.objects.get(id=id_slug)
        except User.DoesNotExist:
            raise Http404

    def get(self, request, id_slug):
        user = self.get_object(id_slug)
        serializer = UserSerializer(user)
        return Response(serializer.data)

    def put(self, request, id_slug):
        user = self.get_object(id_slug)
        serializer = UserSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id_slug):
        user = self.get_object(id_slug)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class RegisterView(views.APIView):
    def post(self, request):
        data = request.data
        hashed_password = bcrypt.hashpw(
            data['password'].encode('utf-8'), bcrypt.gensalt())
        data['password'] = hashed_password.decode('utf-8')
        serializer = UserSerializer(data=data)

        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            data = {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'user': serializer.data
            }
            return custom_response(message='User created successfully', data=data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(views.APIView):
    def post(self, request):
        data = request.data
        email = data.get('email', None)
        password = data.get('password', None)

        if not email or not password:
            return custom_response(message='email and password are required', status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.filter(email=email).first()

        if user is None:
            return custom_response(message='Email or password is incorrect', status=status.HTTP_401_UNAUTHORIZED)

        if not bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
            return custom_response(message='Email or password is incorrect', status=status.HTTP_401_UNAUTHORIZED)

        refresh = RefreshToken.for_user(user)
        serializer = UserSerializer(user)
        data = {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'user': serializer.data
        }
        return custom_response(message='Login successfully', data=data, status=status.HTTP_200_OK)

# class LogoutView(views.APIView):
#     def
