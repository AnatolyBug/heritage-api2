from django.core.mail import EmailMessage
from django.db import IntegrityError
from django.template.loader import render_to_string
from rest_framework import permissions, generics, status
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import PlaceSerializer, CreatePlaceSerializer
from rest_framework import authentication
from random import randint
from .models import Place

class PlaceView(APIView):

    @staticmethod
    def post(request, *args, **kwargs):
        serializer = CreatePlaceSerializer(data=request.data)

        if not serializer.is_valid():
            return Response({
                'message': 'Bad Request',
                'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

        data = serializer.validated_data
        user = request.user

        try:
            Place(**data).save(force_insert=True)
        except:
            return Response({}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

        response = {
            "result": "ok",
            "place": "",
            "links": [{
                "href": f"/place/",
                "rel": "self"
            }]
        }

        return Response(data=data, status=status.HTTP_200_OK)

    @staticmethod
    def get(self, user_id=None):
        return Response(status=status.HTTP_200_OK)

    @staticmethod
    def delete(self):
        pass

    @staticmethod
    def put(self):
        pass