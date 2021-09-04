from django.urls import path
from rest_framework.routers import DefaultRouter
from places import views

router = DefaultRouter()
router.register('types', views.PlaceTypeViewSet, basename='place_type')
router.register('price_category', views.PriceCategoriesViewSet, basename='price_category')
router.register('', views.PlacesViewSet, basename='place')

urlpatterns = [

]

urlpatterns += router.urls
