from rest_framework import serializers
from .models import Booking
from services.models import Service

class BookingSerializer(serializers.ModelSerializer):
    services = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Service.objects.all(),
    )
    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['address'] = instance.branch.address
        data['user'] = {
            'id': instance.user.id,
            'name': instance.user.name,
            'phone': instance.user.phone_number,
        }
        data['services'] = [
            {
                'id': service.id,
                'name': service.name,
                'price': float(service.price),
            }
            for service in instance.services.all()
        ]
        return data
    
    def save(self, **kwargs):
        kwargs['branch'] = self.context['branch']
        kwargs['user'] = self.context['user']
        return super().save(**kwargs)
    class Meta:
        model = Booking
        fields = ['id', 'user', 'branch', 'services', 'datetime', 'status']
        extra_kwargs = {
            'user': {'read_only': True},
            'branch': {'read_only': True}
        }