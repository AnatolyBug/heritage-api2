from django.urls import path, include
from rest_framework.routers import DefaultRouter
from places import views

router = DefaultRouter()

urlpatterns = [
    path('', views.PlaceView.as_view(), name='pace_create'),
]
urlpatterns += router.urls
