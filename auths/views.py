from django.core.mail import EmailMessage
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.db import IntegrityError
from django.utils.encoding import force_bytes, force_text
from django.template.loader import render_to_string
from rest_framework import permissions, generics, status
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import User
from .utils import TokenGenerator
from .serializers import MyTokenObtainPairSerializer, UserSerializer, CreateUserSerializer
from random import randint


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


class UserInfoAPIView(generics.RetrieveAPIView, generics.UpdateAPIView):
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user

    def put(self, request, *args, **kwargs):
        user = request.user
        user.first_name = request.data['first_name']
        user.last_name = request.data['last_name']
        user.email = request.data['email']
        user.save()

        return Response(data=self.get_serializer(user).data)

    def patch(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


class UserSingUpView(APIView):
    permission_classes = (permissions.AllowAny,)

    @staticmethod
    def post(request, *args, **kwargs):
        serializer = CreateUserSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({
                'message': 'Some fields are missing',
                'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        data = serializer.validated_data
        try:
            user = User.objects.create(
                email=data['email'], first_name=data['first_name'], username=data['username'].lower(),
                last_name=data['last_name'], bio=data['bio'])
            user.set_password(data['password'])
            user.save()
        except IntegrityError as e:
            return Response({
                'message': 'This user already exists.',
                'errors': {'Email or Username already exists.'}
            }, status=status.HTTP_400_BAD_REQUEST)

        email_verification_url = '%s/api/auth/email_verification?uid=%s&token=%s' % (
            request.build_absolute_uri('/')[:-1],
            urlsafe_base64_encode(force_bytes(user.pk)),
            TokenGenerator().make_token(user)
        )
        try:
            name = user.first_name + ' ' + user.last_name
            message = render_to_string('email_verification.html', {
                'name': name,
                'email_verification_url': email_verification_url
            })

            email = EmailMessage(
                'Email verification', message, to=[user.email]
            )
            email.send()
        except Exception:
            pass

        return Response(data=UserSerializer(user).data, status=status.HTTP_201_CREATED)


class EmailVerificationView(APIView):
    permission_classes = (permissions.AllowAny,)

    @staticmethod
    def post(request):
        try:
            uid = force_text(urlsafe_base64_decode(request.data['uid']))
            user = User.objects.get(pk=uid)
            if user is None or not TokenGenerator().check_token(user, request.data['token']):
                return Response(status=status.HTTP_400_BAD_REQUEST)
            user.email_confirmed = True
            user.save()
        except Exception:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_204_NO_CONTENT)
