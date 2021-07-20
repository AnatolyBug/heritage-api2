from django.core.mail import EmailMessage
from django.db import IntegrityError
from django.template.loader import render_to_string
from rest_framework import permissions, generics, status
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import User
from .serializers import PlaceSerializer, CreatePlaceSerializer
from rest_framework import authentication
from random import randint

class PlaceView(APIView):

    authentication_classes = [authentication.TokenAuthentication]

    @staticmethod
    def post(request, *args, **kwargs):
        serializer = CreatePlaceSerializer(data=request.data)

    @staticmethod
    def get(self):
        pass

    @staticmethod
    def delete(self):
        pass

    @staticmethod
    def put(self):
        pass