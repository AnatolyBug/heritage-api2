from django.urls import path
from rest_framework.routers import DefaultRouter
from places import views

router = DefaultRouter()

urlpatterns = [
    path('place/', views.PlaceView.as_view(), name='place'),
    path('place/<place_id>', views.PlaceView.as_view(), name='place')
]

urlpatterns += router.urls