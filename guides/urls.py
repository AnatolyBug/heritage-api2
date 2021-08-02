from django.urls import path
from rest_framework.routers import DefaultRouter
from guides import views

router = DefaultRouter()
router.register('friendly_tags', views.FriendlyTagViewSet, basename='friendly_tag')
router.register('transport_methods', views.TransportMethodViewSet, basename='transport_method')
router.register('', views.GuideViewSet, basename='guide')

urlpatterns = [
    # path('place/', views.PlaceView.as_view(), name='place'),
    # path('place/<place_id>', views.PlaceView.as_view(), name='place')
]

urlpatterns += router.urls
