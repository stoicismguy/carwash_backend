from django.urls import path
from .views import BookingView, get_available_hours

urlpatterns = [
    path('', BookingView.as_view(), name="RC Броинрование"),
    path('<int:pk>/hours/', get_available_hours, name='Доступные часы'),
]