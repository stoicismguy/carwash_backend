from rest_framework.serializers import ModelSerializer
from .models import Carwash, Rating, Branch


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


class BranchSerializer(ModelSerializer):

    def save(self, **kwargs):
        kwargs['carwash'] = self.context['carwash']
        return super().save(**kwargs)
    class Meta:
        model = Branch
        fields =  '__all__'
        extra_kwargs = {
            'rating': { 'read_only': True },
            'created_at': { 'read_only': True }
        }


class RatingSerializer(ModelSerializer):
    def save(self, **kwargs):
        kwargs['user'] = self.context['user']
        kwargs['branch'] = self.context['branch']
        return super().save(**kwargs)
    class Meta:
        model = Rating
        fields =  '__all__'
        extra_kwargs = {
            'user': { 'read_only': True },
            'branch': { 'read_only': True },
            'created_at': { 'read_only': True },
            'description': { 'required': False }
        }