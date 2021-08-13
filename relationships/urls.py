from django.urls import path
from rest_framework.routers import DefaultRouter
from relationships import views

router = DefaultRouter()
router.register('', views.RelationshipViewSet, basename='relationship')

urlpatterns = [
    path('follow/', views.FollowRelationshipView.as_view(), name='follow'),
]

urlpatterns += router.urls
