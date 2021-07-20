from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework.routers import DefaultRouter
from auths import views

router = DefaultRouter()

urlpatterns = [
    path('login/', views.MyTokenObtainPairView.as_view(), name='login'),
    path('register/', views.UserSingUpView.as_view(), name='register'),
    path('email_verification/', views.EmailVerificationView.as_view(), name='email_verification'),
    path('token-refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]

urlpatterns += router.urls
