import os
from rest_framework import serializers, status
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import authenticate
from django.utils.six import text_type
from rest_framework.response import Response
from .models import User
from utils.aws import generate_aws_url
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError


username_validator = RegexValidator("^[a-zA-Z0-9_.-]{4,25}$",
                                    "username can only contain alphanumeric characters, ., _,-")
password_validator = RegexValidator("^(?=.*[0-9])(?=.*[a-z])(?=.*[A-Z]).{8,32}$",
                                    "password must contain at least an Uppercase, lowercase and a number, "
                                    "and be at least 8 chars long")


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        self.user = authenticate(**{
            self.username_field: attrs[self.username_field],
            'password': attrs['password'],
        })

        if self.user is None:
            raise serializers.ValidationError('register')

        if not self.user.email_confirmed:
            raise serializers.ValidationError('email_verification')

        refresh = self.get_token(self.user)

        return {
            'email': self.user.email,
            'refresh': text_type(refresh),
            'access': text_type(refresh.access_token),
        }

class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True, validators=[password_validator])
    new_password = serializers.CharField(required=True, validators=[password_validator])

class ResendEmailSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True, validators=[password_validator])

class ResetPasswordSerializer(serializers.Serializer):
    uid = serializers.CharField(required=True)
    token = serializers.CharField(required=True)
    password = serializers.CharField(required=True, validators=[password_validator])

class BaseUserSerializer(serializers.ModelSerializer):
    avatar_url = serializers.SerializerMethodField()

    def get_avatar_url(self, obj):
        bucket_name = os.getenv('AWS_AVATAR_IMAGE_BUCKET_NAME')
        content_type = 'image/png'
        return generate_aws_url(key=obj.avatar_filename, bucket=bucket_name, content_type=content_type)

class UserSerializer(BaseUserSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'username', 'user_role', 'first_name',
                           'last_name', 'bio', 'avatar_url', 'created_date')


class PutUserSerializer(serializers.Serializer):
    email = serializers.EmailField(required=False)
    username = serializers.CharField(validators=[username_validator])
    first_name = serializers.CharField(required=False, allow_blank=True)
    last_name = serializers.CharField(required=False, allow_blank=True)
    bio = serializers.CharField(required=False, allow_blank=True)
    file = serializers.CharField(required=False, allow_blank=True)

class CreateUserSerializer(serializers.Serializer):
    email = serializers.EmailField()
    username = serializers.CharField(validators=[username_validator])
    password = serializers.CharField(validators=[password_validator])

    def validate(self, attrs):
        unknown = set(self.initial_data) - set(self.fields)
        if unknown:
            raise ValidationError("Unknown field(s): {}".format(", ".join(unknown)))
        return attrs
