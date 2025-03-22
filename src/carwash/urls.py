from rest_framework.routers import DefaultRouter
from django.urls import path
from .views import CarwashView, CarwashDetailView

router = DefaultRouter()
# router.register(r'', CarwashView)

urlpatterns = [
    path('', CarwashView.as_view()),
    path('<int:pk>/', CarwashView.as_view()),
    path('<int:pk>/ratings/', CarwashDetailView.as_view()),
    path('ratings/<int:review_id>/', CarwashDetailView.as_view()),
]

urlpatterns += router.urls
