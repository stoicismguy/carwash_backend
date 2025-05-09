from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.db.models import Q, Sum
import datetime
from django.utils import timezone
from .serializers import BookingSerializer
from .models import Booking
from carwash.models import Branch
from services.models import Service


class BookingView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        branch = get_object_or_404(Branch, pk=pk)
        date_str = request.query_params.get('date')
        
        bookings = Booking.objects.filter(branch=branch)
        
        if date_str:
            try:
                date = datetime.datetime.strptime(date_str, '%Y-%m-%d').date()
                bookings = bookings.filter(datetime__date=date)
            except ValueError:
                return Response({'error': 'Неверный формат даты. Используйте YYYY-MM-DD'}, status=400)
                
        return Response(BookingSerializer(bookings, many=True).data)
    

    def post(self, request, pk):
        branch = get_object_or_404(Branch, pk=pk)
        serializer = BookingSerializer(data=request.data, context={'branch':branch})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)



@api_view(['POST'])
@permission_classes([AllowAny])
def get_available_hours(request, pk):
    date_str = request.data.get('date')
    service_ids = request.data.get('services')
    if not date_str or not service_ids:
        return Response({'error': 'Дата и услуги обязательны'}, status=400)
    services = Service.objects.filter(pk__in=service_ids)
    if services.count() != len(service_ids):
        return Response({'error': 'Не все выбранные услуги существуют'}, status=404)
    duration = services.aggregate(total=Sum('duration')).get('total')
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
        available_hours.extend(
            _split_timings(
                branch.opening_time,
                branch.closing_time,
                duration=duration,
                date=date
            )
        )
        return Response(available_hours, status=200)

    for i in range(0, len(bookings)):
        if i == 0:
            available_hours.extend(
                _split_timings(
                    branch.opening_time,
                    bookings.first().datetime.time(),
                    duration=duration,
                    date=date)
            )
            if len(bookings) != 1:
                continue

        if i == len(bookings) - 1:
            available_hours.extend(
                _split_timings(
                    bookings.last().datetime + bookings.last().total_duration,
                    branch.closing_time,
                    duration=duration,
                    date=date)
            )
            continue

        booking = bookings[i]
        next_booking = bookings[i+1]
        available_hours.extend(
            _split_timings(
                booking.datetime.time(),
                next_booking.datetime.time() + next_booking.total_duration,
                duration=duration,
                date=date
            )
        )
        
    return Response(available_hours, status=200)


def _split_timings(start, end, duration, space=timezone.timedelta(minutes=30), date=datetime.datetime(2020, 1, 1)) -> list:
    if (isinstance(start, datetime.time)):
        start = datetime.datetime.combine(date, start)
    if (isinstance(end, datetime.time)):
        end = datetime.datetime.combine(date, end)

    if (end - start < duration):
        return []
    
    result = []
    cs_start = start
    finish = end - duration
    print(start, end)

    while cs_start + space <= finish:
        result.append({
            'start': cs_start,
            'end': (cs_start + space),
            'display': cs_start.time()
        })
        cs_start += space

    return result


@api_view(['POST'])
@permission_classes([AllowAny])
def make_booking(request, pk):
    serivces = request.data.get('services')
    date = request.data.get('datetime')

    branch = get_object_or_404(Branch, pk=pk)

    if not serivces or not date:
        return Response({'error': 'Необходимо указать services и date'}, status=400)
    
    services = Service.objects.filter(pk__in=serivces)
    if services.count() != len(serivces):
        return Response({'error': 'Не все выбранные услуги существуют'}, status=404)
    
    duration = services.aggregate(total=Sum('duration')).get('total')
    if not duration:
        return Response({'error': 'Не удалось рассчитать продолжительность бронирования'}, status=400)
    
    booking_time = datetime.datetime.fromisoformat(date)
    if booking_time < timezone.now():
        return Response({'error': 'Невозможно забронировать прошедшее время'}, status=400)
    
    # booking_end = booking_time + datetime.timedelta(minutes=duration)
    # conflicting_bookings = Booking.objects.filter(
    #     branch=branch,
    #     datetime__lte=booking_time,
    #     datetime__gt=booking_time - datetime.timedelta(minutes=duration)
    # ).exists() or Booking.objects.filter(
    #     branch=branch,
    #     datetime__lt=booking_end,
    #     datetime__gte=booking_time
    # ).exists()

    # if conflicting_bookings.exists():
    #     return Response({'error': 'На выбранное время уже есть бронирование'}, status=400)

    serializer = BookingSerializer(data=request.data, context={
            'branch': branch,
            'user': request.user
        })
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_history(request):
    bookings = Booking.objects.filter(user=request.user).order_by('-datetime')
    return Response(BookingSerializer(bookings, many=True).data, status=200)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def get_bookings_by_date(request, pk):
    branch = get_object_or_404(Branch, pk=pk)
    date_str = request.data.get('date')
    
    if not date_str:
        return Response({'error': 'Дата обязательна'}, status=400)
    
    try:
        date = datetime.datetime.strptime(date_str, '%Y-%m-%d').date()
        bookings = Booking.objects.filter(branch=branch, datetime__date=date).prefetch_related('services').select_related('user')
        return Response(BookingSerializer(bookings, many=True).data)
    except ValueError:
        return Response({'error': 'Неверный формат даты. Используйте YYYY-MM-DD'}, status=400)

