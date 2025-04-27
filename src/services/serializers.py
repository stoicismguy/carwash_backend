from rest_framework.serializers import ModelSerializer, SerializerMethodField
from .models import Service, ServiceGroup, Bodytype


class ServiceSerializer(ModelSerializer):

    def save(self, **kwargs):
        kwargs['group'] = self.context['group']
        return super().save(**kwargs)

    class Meta:
        model = Service
        fields = '__all__'



class ServiceGroupSerializer(ModelSerializer):
    services_count = SerializerMethodField('get_services_count')
    services = SerializerMethodField('get_services')

    def get_services(self, obj):
        return ServiceSerializer(Service.objects.filter(group=obj), many=True).data

    def get_services_count(self, obj):
        return Service.objects.filter(group=obj).count()
    
    def save(self, **kwargs):
        kwargs['branch'] = self.context['branch']
        return super().save(**kwargs)

    class Meta:
        model = ServiceGroup
        fields = ['id', 'branch', 'name', 'services', 'services_count']
        extra_kwargs = {
            'services_count': {'read_only': True},
            'services': {'read_only': True}
        }

class BodytypeSerializer(ModelSerializer):
    class Meta:
        model = Bodytype
        fields = '__all__'