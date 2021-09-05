from django.urls import path
from rest_framework.routers import DefaultRouter
from admins import views

router = DefaultRouter()
router.register('users', views.AdminUserViewSet, basename='place_type')

urlpatterns = []

urlpatterns += router.urls