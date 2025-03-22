from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from .serializers import CarwashSerializer, RatingSerializer
from .models import Carwash, Rating
from settings.permissions import BusinessOnly


class CarwashView(APIView):
    permission_classes = [IsAuthenticated, BusinessOnly]

    def get_permissions(self):
        if self.request.method == 'GET':
            return [AllowAny()]
        return super().get_permissions()
    
    def get(self, request):
        # TODO: Добавить фильтрацию
        queryset = Carwash.objects.all()
        serializer = CarwashSerializer(queryset, many=True)
        return Response(serializer.data, status=200)
    
    def post(self, request):
        serializer = CarwashSerializer(data=request.data, context={'user':request.user})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)
    
    def delete(self, request, pk):
        carwash = get_object_or_404(Carwash, pk=pk)
        if carwash.user != request.user:
            return Response({'error': 'У вас нет доступа для удаления'}, status=403)
        carwash.delete()
        return Response({'message': 'Успешно удалено'}, status=200)
    
    def put(self, request, pk):
        carwash = get_object_or_404(Carwash, pk=pk)
        if carwash.user != request.user:
            return Response({'error': 'У вас нет доступа для обновления'}, status=403)
        serializer = CarwashSerializer(carwash, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=200)
        return Response(serializer.errors, status=400)
    

class CarwashDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        if self.request.method == 'GET':
            return [AllowAny()]
        return super().get_permissions()

    def get(self, request, pk):
        carwash = get_object_or_404(Carwash, pk=pk)
        ratings = carwash.received_ratings.all()
        serializer = RatingSerializer(ratings, many=True)
        return Response(serializer.data, status=200)
    
    def post(self, request, pk):
        carwash = get_object_or_404(Carwash, pk=pk)
        serializer = RatingSerializer(data=request.data, context={'user':request.user, 'carwash':carwash})
        if serializer.is_valid():
            serializer.save()
            carwash.update_rating()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)
    

    def delete(self, request, review_id):
        rating = get_object_or_404(Rating, pk=review_id)
        if rating.user != request.user:
            return Response({'error': 'У вас нет доступа для удаления'}, status=403)
        rating.delete()
        return Response({'message': 'Успешно удалено'}, status=200)