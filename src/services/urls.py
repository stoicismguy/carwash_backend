from django.urls import path
from .views import ServicesView, ServiceDetailView

urlpatterns = [
    path('<int:pk>/', ServicesView.as_view(), name='Услуги автомойки'),
]