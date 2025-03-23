from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.urls import path
from .views import UserViewSet, UserView, register
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
# router.register(r'', UserViewSet)


urlpatterns = [
    path('', UserView.as_view()),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', register, name='register'),
]

urlpatterns += router.urls