from django.urls import path
from rest_framework.routers import DefaultRouter
from relationships import views

router = DefaultRouter()
router.register('', views.RelationshipViewSet, basename='relationship')

urlpatterns = [
    path('admin/', views.RelationshipAdminViewSet, name='follow'),
]

urlpatterns += router.urls
