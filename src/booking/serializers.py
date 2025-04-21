from rest_framework import serializers
from .models import Booking
from services.models import Service

class BookingSerializer(serializers.ModelSerializer):
    services = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Service.objects.all()
    )
    class Meta:
        model = Booking
        fields = ['id', 'user', 'branch', 'services', 'datetime', 'status']