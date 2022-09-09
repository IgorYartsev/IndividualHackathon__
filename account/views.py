from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import permissions,generics

from django.contrib.auth import get_user_model

from . import serializers
from .permissions import IsAccountOwner
from my_movies.tasks import send_email_task,send_reset_email_task

User = get_user_model()

class RegistrationView(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self ,request):
        serializer = serializers.RegistrerSerializer(data = request.data)
        if serializer.is_valid(raise_exception = True):
            user = serializer.save()
            if user:
                send_email_task.delay(user.email, user.activation_code)
            return Response (serializer.data, status = 201)
        return Response (status=400)

class ActivationView(APIView):
    permission_classes = (permissions.AllowAny,)
    def get(self, request, activation_code):
        try:
            user = User.objects.get(activation_code = activation_code)
            user.is_active = True
            user.activation_code = ''
            user.save()
            return Response({
                'msg':'Successfully activated!'},
                status=200,
            )
        except User.DoesNotExist :
            return Response(
                {'msg':'Link expired!'},
                status = 400,
            )

class LoginApiView(TokenObtainPairView):
    serializer_class = serializers.LoginSerializer


class LogoutApiView(GenericAPIView):
    serializer_class = serializers.LogoutSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def post(self , request, *args):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response('Successfully loged out', status = 204)

class ForgorPasswordView(APIView):
    permission_classes = (permissions.AllowAny,)
    def post(self, request):
        serializer = serializers.ForgotPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            user = User.objects.get(email = serializer.data.get(('email')))
            user.create_activation_code()
            user.save()
            send_reset_email_task.delay(user.email,user.activation_code)
            return Response('Chek your mail!',status=200)
        except User.DoesNotExist:
            return Response('User with this email does not exist',
            status=400)

class RestorePasswordView(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        serializer = serializers.RestorePasswordSerializer(data =request.data)
        serializer.is_valid(raise_exception = True)
        serializer.save()

        return Response('Password chaneged successfully', status = 200)



class SendingMessagesView(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self,request):
        serializer = serializers.SendingMessagesSerializers(data= request.data)
        serializer.is_valid(raise_exception = True)
        serializer.save()
        return Response('You have subscribed to the mailing list',status=200)



class UserDetailView(generics.RetrieveAPIView):
    queryset = User.objects.all()
    permission_classes = (permissions.IsAuthenticated,IsAccountOwner)
    serializer_class = serializers.UserSerializer






