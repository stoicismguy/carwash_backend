from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.db.models import Q, Sum
import datetime

from .serializers import BookingSerializer
from .models import Booking
from carwash.models import Branch
from services.models import Service


class BookingView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        branch = get_object_or_404(Branch, pk=pk)
        bookings = Booking.objects.filter(branch=branch)
        return Response(BookingSerializer(bookings, many=True).data)
    

    def post(self, request, pk):
        branch = get_object_or_404(Branch, pk=pk)
        serializer = BookingSerializer(data=request.data, context={'branch':branch})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


@api_view(['GET'])
@permission_classes([AllowAny])
def get_available_hours(request, pk):
    date_str = request.data.get('date')
    service_ids = request.data.get('services')
    print(service_ids)
    if not date_str or not service_ids:
        return Response({'error': 'Дата и услуги обязательны'}, status=400)
    services = Service.objects.filter(pk__in=service_ids)
    if services.count() != len(service_ids):
        return Response({'error': 'Не все выбранные услуги существуют'}, status=404)
    duration = services.aggregate(total=Sum('duration')).get('total')
    print(duration, type(duration))
    branch = get_object_or_404(Branch, pk=pk)
    date = datetime.datetime.strptime(date_str, '%Y-%m-%d').date()
    bookings = Booking.objects.filter(
        branch=branch,
        datetime__date=date
    ).prefetch_related('services').annotate(
        total_duration=Sum('services__duration')
    )
    available_hours = []
    if bookings.count() == 0:
        available_hours.append({
            'start': branch.opening_time,
            'end': branch.closing_time
        })
        return Response(available_hours, status=200)

    if datetime.datetime.combine(date, branch.opening_time) + duration <= bookings[0].datetime:
        available_hours.append({
            'start': branch.opening_time,
            'end': bookings[0].datetime
    })
    for i in range(len(bookings)-1):
        booking = bookings[i]
        next_booking = bookings[i+1]
        if next_booking.datetime - booking.datetime + booking.total_duration >= duration:
            available_hours.append({
                'start': booking.datetime + booking.total_duration,
                'end': next_booking.datetime
            })
    if branch.closing_time - duration >= bookings[-1].datetime:
        available_hours.append({
            'start': branch.closing_time,
            'end': bookings[-1].datetime
    })
        
    return Response(available_hours, status=200)


