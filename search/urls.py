from django.urls import path
from rest_framework.routers import DefaultRouter
from search import views

router = DefaultRouter()

urlpatterns = [
    path('user/', views.UserSearchView.as_view(), name='search'),
]

urlpatterns += router.urls
