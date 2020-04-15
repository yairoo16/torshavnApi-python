from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token
# from rest_framework_simplejwt.views import (
#     TokenObtainPairView,
#     TokenRefreshView,
# )

from torshavn_api import views

router = DefaultRouter()
router.register('hello-viewset', views.HelloViewSet, basename='hello-viewset')
router.register('user', views.UserViewSet)
router.register('feed', views.UserFeedViewSet)
router.register('marker', views.MarkerViewSet, basename='marker')

urlpatterns = [
    path('hello-view/', views.HelloApiView.as_view()),
    path('login/', obtain_jwt_token),
    path('refresh-token/', refresh_jwt_token),
    # path('login/', views.UserLoginApiView.as_view()),
    # path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    # path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('', include(router.urls))
]