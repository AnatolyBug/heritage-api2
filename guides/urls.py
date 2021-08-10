from django.urls import path
from rest_framework.routers import DefaultRouter
from guides import views
from comments.views import CommentsViewSet

router = DefaultRouter()
router.register('', views.GuideViewSet, basename='guide')
router.register('friendly_tags', views.FriendlyTagViewSet, basename='friendly_tag')
router.register('transport_methods', views.TransportMethodViewSet, basename='transport_method')
router.register('comments', CommentsViewSet, basename='comment')

urlpatterns = [
    path('feed/', views.FeedView.as_view(), name='feed'),
    # path('place/<place_id>', views.PlaceView.as_view(), name='place')
]

urlpatterns += router.urls
