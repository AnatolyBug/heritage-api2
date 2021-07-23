from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework.routers import DefaultRouter
from auths import views

router = DefaultRouter()

urlpatterns = [
    path('login/', views.MyTokenObtainPairView.as_view(), name='login'),
    path('register/', views.UserSingUpView.as_view(), name='register'),
    path('user/', views.UserInfoAPIView.as_view(), name='user_info'),
    path('forgot_password/', views.ForgotPasswordView.as_view(), name='forgot_password'),
    path('reset_password/', views.ResetPasswordView.as_view(), name='forgot_password'),
    path('email_verification', views.EmailVerificationView.as_view(), name='email_verification'),
    path('token-refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]

urlpatterns += router.urls
