from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework.routers import DefaultRouter
import views

router = DefaultRouter()

urlpatterns = [
    path('auth/login', views.MyTokenObtainPairView.as_view(), name='login'),
    path('auth/register', views.UserSingUpView.as_view(), name='register'),
    path('auth/token-refresh', TokenRefreshView.as_view(), name='token_refresh'),
]

urlpatterns += router.urls
