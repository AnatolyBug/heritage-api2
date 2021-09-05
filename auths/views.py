import os
import time
import base64
from django.core.mail import EmailMessage
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.utils.encoding import force_bytes, force_text
from django.utils.decorators import method_decorator
from django.template.loader import get_template
from rest_framework import permissions, generics, status
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import User
from utils.auth import TokenGenerator
from utils.aws import upload_file_to_aws
from django.conf import settings
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from .serializers import MyTokenObtainPairSerializer, UserSerializer, CreateUserSerializer, \
    ChangePasswordSerializer, ResendEmailSerializer, ResetPasswordSerializer, LoginSerializer, PutUserSerializer

@method_decorator(name="post", decorator=swagger_auto_schema(request_body=LoginSerializer,
                  responses={"200": openapi.Response(description="Login",
                  examples={"application/json": {'email': '', 'Refresh': '', 'token': ''}}),
                  "400": openapi.Response(description="ValidationError")}))
class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

class UserInfoAPIView(APIView):
    http_method_names = ['get', 'post', 'put', 'delete']
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = UserSerializer

    @swagger_auto_schema(request_body=PutUserSerializer, operation_description='User to view their profile',
                         responses={"200": serializer_class})
    def get(self, pk):
        return Response(data=self.serializer_class(self.request.user).data, status=status.HTTP_200_OK)

    @swagger_auto_schema(request_body=PutUserSerializer,
                         responses={"200": serializer_class, "400": ''},
                         operation_description='User to update their profile')
    def put(self, request, *args, **kwargs):
        serializer = PutUserSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({
                'errors': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)
        data = serializer.validated_data
        # https://stackoverflow.com/questions/46194898/attributeerror-price-object-has-no-attribute-update
        user = User.objects.filter(pk=request.user.pk)

        try:
            avatar_file = data.pop('file', None)
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
                data.avatar_filename = avatar_file_name
            user.update(**data)

        except IntegrityError:
            return Response({'error': 'Username already exists'}, status=status.HTTP_400_BAD_REQUEST)

        return Response(data=self.serializer_class(request.user).data, status=status.HTTP_200_OK)

    @swagger_auto_schema(operation_description='User or Admin to delete profile')
    def delete(self, request, pk=None):
        user = User.objects.filter(pk=pk, is_active=True).first()
        if not user:
            Response({'error': 'no such user'}, status=status.HTTP_400_BAD_REQUEST)
        if user.id == request.user.id or request.user.is_staff:
            user.is_active = False
            user.save()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_400_BAD_REQUEST)


class UserSingUpView(APIView):
    permission_classes = (permissions.AllowAny,)

    response_schema_dict = {
        "200": openapi.Response(description="Successfully created User"),
        "400": openapi.Response(
            description="ValidationError",
            examples={"application/json": {'error': 'Email or Username already exists'}})}

    @swagger_auto_schema(
        request_body=CreateUserSerializer, responses=response_schema_dict,
        operation_description='User registaration')
    def post(self, request, *args, **kwargs):
        serializer = CreateUserSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({
                'errors': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)
        data = serializer.validated_data
        try:
            user = User.objects.create(username=data['username'].lower(), email=data['email'])
            user.set_password(data['password'])
            user.save()
        except IntegrityError as e:
            return Response({
                'error': 'Email or Username already exists'
            }, status=status.HTTP_400_BAD_REQUEST)

        email_verification_url = '%s/api/auth/email_verification?uid=%s&token=%s' % (
            request.build_absolute_uri('/')[:-1],
            urlsafe_base64_encode(force_bytes(user.pk)),
            TokenGenerator().make_token(user)
        )

        if not settings.TEST:
            try:
                message_body = ({
                    'name': user.username,
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

        response = {}
        response['email_verification_url'] = email_verification_url if settings.TEST else 'emailed'
        return Response(data=response, status=status.HTTP_201_CREATED)


class EmailVerificationView(APIView):
    permission_classes = (permissions.AllowAny,)
    uid_param = openapi.Parameter('uid', openapi.IN_QUERY, description="secret id", type=openapi.TYPE_STRING)
    token_param = openapi.Parameter('token', openapi.IN_QUERY, description="secret id", type=openapi.TYPE_STRING)

    @swagger_auto_schema(manual_parameters=[uid_param, token_param],
                         responses={'302': 'redirect to /login', '400': "Bad verification URL"
        }, operation_description='User to Verify their Email')
    def get(self, request):
        try:
            uid = force_text(urlsafe_base64_decode(request.query_params['uid']))
            user = User.objects.get(pk=uid)
            if user is None or not TokenGenerator().check_token(user, request.query_params['token']):
                return Response(status=status.HTTP_400_BAD_REQUEST)
            user.email_confirmed = True
            user.save()
        except Exception:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        return HttpResponseRedirect('/login')


class ResendEmailView(APIView):
    permission_classes = (permissions.AllowAny,)
    response_schema_dict = {
        "200": openapi.Response(description="Successfully sent",
                                examples={"application/json": {'result': 'Successfully sent'}}),
        "400": openapi.Response(description="already verified or no such user exists",
            examples={"application/json": {'error': 'already verified or no such user'}})}

    @swagger_auto_schema(request_body=ResendEmailSerializer, responses=response_schema_dict,
                         operation_description='User to Resend Verification Email')
    def post(self, request):
        email = request.data['email']
        user = User.objects.filter(email=email).first()

        if user and not user.email_confirmed:
            email_verification_url = '%s/api/auth/email_verification?uid=%s&token=%s' % (
                request.build_absolute_uri('/')[:-1],
                urlsafe_base64_encode(force_bytes(user.pk)),
                TokenGenerator().make_token(user)
            )

            if not settings.TEST:
                try:
                    message_body = ({
                        'name': user.username,
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

            data = {'result': 'Successfully sent'}
            data['email_verification_url'] = email_verification_url if settings.TEST else ''
            return Response(data=data, status=status.HTTP_200_OK)

        elif user and user.email_confirmed:
            return Response(data={'error': 'already verified'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(data={'error': 'no such user'}, status=status.HTTP_400_BAD_REQUEST)


class ForgotPasswordView(APIView):
    permission_classes = (permissions.AllowAny,)
    response_schema_dict = {
        "200": openapi.Response(description="Successfully sent",
                                examples={"application/json": {'result': 'Successfully sent'}}),
        "403": openapi.Response(description="user needs to verify email first",
                                examples={"application/json": {'error': 'unverified'}}),
        "404": openapi.Response(description="no user with such email",
                                examples={"application/json": {'error': 'no such user'}})}

    @swagger_auto_schema(request_body=ResendEmailSerializer, responses=response_schema_dict,
                         operation_description='User to get email with password reset link. Must be verified')
    def post(self, request):
        email = request.data['email']
        user = User.objects.filter(email=email).first()

        if user and user.email_confirmed:
            password_reset_url = '%s/login/reset_password?uid=%s&token=%s' % (
                request.build_absolute_uri('/')[:-1],
                urlsafe_base64_encode(force_bytes(user.pk)),
                TokenGenerator().make_token(user)
            )

            if not settings.TEST:
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

            data = {'result': 'Successfully sent'}
            data['password_reset_url'] = password_reset_url if settings.TEST else ''
            return Response(data=data, status=status.HTTP_200_OK)
        elif user and not user.email_confirmed:
            return Response(data={'error': 'unverified'}, status=status.HTTP_403_FORBIDDEN)
        else:
            return Response(data={'error': 'no such user'}, status=status.HTTP_404_NOT_FOUND)


class ResetPasswordView(APIView):
    permission_classes = (permissions.AllowAny,)
    response_schema_dict = {
        "204": openapi.Response(description="password changed"),
        "400": openapi.Response(description="validation error",
                                examples={"application/json": {'error': 'issues with request'}})}

    @swagger_auto_schema(request_body=ResetPasswordSerializer,
                         responses=response_schema_dict,
                         operation_description='User to reset password with the link from the email')
    def post(self, request):
        serializer = ResetPasswordSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({
                'error': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)

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
    response_schema_dict = {
        "200": openapi.Response(description="Password updated successfully",
                                examples={"application/json": {'result': 'Password updated successfully'}}),
        "400": openapi.Response(description="validation error",
                                examples={"application/json": {'error': 'Old password is wrong'}})}

    @swagger_auto_schema(request_body=ChangePasswordSerializer,
                         responses=response_schema_dict,
                         operation_description='User to change their password')
    def post(self, request):
        user_id = request.user.id
        user = User.objects.get(id=user_id)
        serializer = ChangePasswordSerializer(data=request.data)

        if serializer.is_valid():
            if not user.check_password(request.data['old_password']):
                return Response({'error': 'Old password is wrong'}, status=status.HTTP_400_BAD_REQUEST)

            user.set_password(request.data['new_password'])
            user.save()

            return Response({'result': 'Password updated successfully'}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
