from rest_framework.serializers import ModelSerializer
from .models import Carwash, Rating


class CarwashSerializer(ModelSerializer):

    def save(self, **kwargs):
        
        kwargs['user'] = self.context['user']
        return super().save(**kwargs)
    
    class Meta:
        model = Carwash
        fields =  '__all__'
        extra_kwargs = {
            'user': { 'read_only': True },
            'rating': { 'read_only': True },
            'created_at': { 'read_only': True }
        }


class RatingSerializer(ModelSerializer):
    def save(self, **kwargs):
        kwargs['user'] = self.context['user']
        kwargs['carwash'] = self.context['carwash']
        return super().save(**kwargs)
    class Meta:
        model = Rating
        fields =  '__all__'
        extra_kwargs = {
            'user': { 'read_only': True },
            'carwash': { 'read_only': True },
            'created_at': { 'read_only': True }
        }