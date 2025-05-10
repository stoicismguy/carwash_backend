from django.urls import path
from .views import *

urlpatterns = [
    path('', BookingView.as_view(), name="RC Броинрование"),
    path('<int:pk>/hours/', get_available_hours, name='Доступные часы'),
    path('<int:pk>/booking/', make_booking, name='Создание бронирования'),
    path('<int:pk>/booking/by-date/', get_bookings_by_date, name='Бронирования по дате'),
    path('history/', get_history, name='История бронирований'),
    path('<int:pk>/', delete_booking, name='Удаление бронирования'),
]