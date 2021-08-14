import os
import time
import base64
from django.core.mail import EmailMessage
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.db import IntegrityError
from django.utils.encoding import force_bytes, force_text
from django.template.loader import get_template
from rest_framework import permissions, generics, status
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import User
from utils.auth import TokenGenerator
from utils.aws import upload_file_to_aws
from .serializers import MyTokenObtainPairSerializer, UserSerializer, CreateUserSerializer, ChangePasswordSerializer


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


class UserInfoAPIView(generics.RetrieveAPIView, generics.UpdateAPIView, generics.DestroyAPIView):
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user

    def put(self, request, *args, **kwargs):
        user = request.user

        try:
            user.username = request.data['username']
            user.first_name = request.data['first_name']
            user.last_name = request.data['last_name']
            user.email = request.data['email']
            user.bio = request.data['bio']

            avatar_file = request.data['file']

            if avatar_file:
                file_format, img_str = avatar_file.split(';base64,')
                ext = file_format.split('/')[-1]
                avatar_file_name = f"{user.id}_{time.time()}_photo.{ext}"

                with open(avatar_file_name, 'wb') as destination:
                    destination.write(base64.b64decode(img_str))

                bucket_name = os.getenv('AWS_AVATAR_IMAGE_BUCKET_NAME')
                upload = upload_file_to_aws(file_name=avatar_file_name, bucket=bucket_name)

                if upload is True:
                    os.remove(avatar_file_name)

                user.avatar_url = avatar_file_name

            user.save()

        except IntegrityError:
            return Response({'error': 'Username already exists.'}, status=status.HTTP_400_BAD_REQUEST)

        return Response(data=self.get_serializer(user).data, status=status.HTTP_200_OK)

    def patch(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def destroy(self, request, *args, **kwargs):
        user = request.user
        user.is_active = False
        user.save()
        #for some reason test_destroy always returns 200 here
        return Response(data=self.get_serializer(user).data, status=status.HTTP_204_NO_CONTENT)


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

        if os.getenv('TEST') is False:
            try:
                name = user.first_name + ' ' + user.last_name
                message_body = ({
                    'name': name,
                    'email_verification_url': email_verification_url
                })
                message = get_template('email_verification.html').render(message_body)
                email = EmailMessage(
                    'Email verification', message, to=[user.email]
                )
                email.content_subtype = 'html'
                email.send()
            except Exception:
                pass

        response = UserSerializer(user).data
        response['email_verification_url'] = email_verification_url

        return Response(data=response, status=status.HTTP_201_CREATED)


class EmailVerificationView(APIView):
    permission_classes = (permissions.AllowAny,)

    @staticmethod
    def get(request):
        try:
            uid = force_text(urlsafe_base64_decode(request.query_params['uid']))
            user = User.objects.get(pk=uid)
            if user is None or not TokenGenerator().check_token(user, request.query_params['token']):
                return Response(status=status.HTTP_400_BAD_REQUEST)
            user.email_confirmed = True
            user.save()
        except Exception:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_204_NO_CONTENT)


class ForgotPasswordView(APIView):
    permission_classes = (permissions.AllowAny,)

    @staticmethod
    def post(request):
        email = request.data['email']
        check_user = User.objects.filter(email=email).exists()

        if check_user:
            user = User.objects.get(email=email)
            password_reset_url = '%s/login/reset_password?uid=%s&token=%s' % (
                request.build_absolute_uri('/')[:-1],
                urlsafe_base64_encode(force_bytes(user.pk)),
                TokenGenerator().make_token(user)
            )

            if os.getenv('TEST') is False:
                try:
                    name = user.first_name + ' ' + user.last_name
                    message_body = ({
                        'name': name,
                        'password_reset_url': password_reset_url
                    })
                    message = get_template('reset_password.html').render(message_body)
                    email = EmailMessage(
                        'Email verification', message, to=[user.email]
                    )
                    email.content_subtype = 'html'
                    email.send()
                except Exception:
                    pass
            return Response(data={'password_reset_url': password_reset_url},
                            status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)


class ResetPasswordView(APIView):
    permission_classes = (permissions.AllowAny,)

    @staticmethod
    def post(request, *args, **kwargs):
        try:
            uid = force_text(urlsafe_base64_decode(request.data['uid']))
            user = User.objects.get(pk=uid)

            if user is None or not TokenGenerator().check_token(user, request.data['token']):
                return Response(status=status.HTTP_400_BAD_REQUEST)

            user.set_password(request.data['password'])
            user.save()
        except Exception:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        return Response(status=status.HTTP_204_NO_CONTENT)


class ChangePasswordView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    @staticmethod
    def post(request):
        user_id = request.user.id
        user = User.objects.get(id=user_id)
        serializer = ChangePasswordSerializer(data=request.data)

        if serializer.is_valid():
            if not user.check_password(request.data['old_password']):
                return Response({'message': 'Old password is wrong.'}, status=status.HTTP_400_BAD_REQUEST)

            user.set_password(request.data['new_password'])
            user.save()

            return Response({'message': 'Password updated successfully'}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
