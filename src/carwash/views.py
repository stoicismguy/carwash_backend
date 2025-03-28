from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.db.models import Q

from .serializers import CarwashSerializer, RatingSerializer, BranchSerializer
from .models import Carwash, Rating, Branch
from services.models import Bodytype
from services.serializers import BodytypeSerializer
from settings.permissions import BusinessOnly



class CarwashView(APIView):
    # TODO: Пофиксить AllowAny для мертвого access токена
    permission_classes = [IsAuthenticated, BusinessOnly]

    def get_permissions(self):
        if self.request.method == 'GET':
            return [AllowAny()]
        return super().get_permissions()
    
    def get(self, request):
        queryset = Carwash.objects.all()

        if active := request.data.get('active', True):
            if active: queryset = queryset.filter(is_active=active)
            else: pass

        serializer = CarwashSerializer(queryset, many=True)
        return Response(serializer.data, status=200)
    
    def post(self, request):
        serializer = CarwashSerializer(data=request.data, context={'user':request.user})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)
    
class CarwashDetailView(APIView):
    permission_classes = [IsAuthenticated, BusinessOnly]

    def get_permissions(self):
        if self.request.method == 'GET':
            return [AllowAny()]
        return super().get_permissions()
    
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

@api_view(['GET'])
@permission_classes([AllowAny])
def get_carwash_bodytypes(request, pk):
    carwash = get_object_or_404(Carwash, pk=pk)
    bodytypes = Bodytype.objects.filter(
        Q(branch_bodytypes__carwash=carwash) & Q(branch_bodytypes__is_active=True)
    ).distinct().order_by('id')
    return Response(BodytypeSerializer(bodytypes, many=True).data)

class RatingsView(APIView):
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        if self.request.method == 'GET':
            return [AllowAny()]
        return super().get_permissions()

    def get(self, request, pk):
        carwash = get_object_or_404(Carwash, pk=pk)
        branches = Branch.objects.filter(carwash=carwash).prefetch_related('received_ratings')
        all_ratings = [rating for branch in branches for rating in branch.received_ratings.all()]
        serializer = RatingSerializer(all_ratings, many=True)
        return Response(serializer.data, status=200)


class RatingBranchView(APIView):
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        if self.request.method == 'GET':
            return [AllowAny()]
        return super().get_permissions()
    
    def get(self, request, pk):
        branch = get_object_or_404(Branch, pk=pk)
        serializer = RatingSerializer(branch.received_ratings.all(), many=True)
        return Response(serializer.data, status=200)
    
    def post(self, request, pk):
        # TODO: Добавить обновление рейтинга
        branch = get_object_or_404(Branch, pk=pk)
        serializer = RatingSerializer(data=request.data, context={'user':request.user, 'branch':branch})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)
    

class RatingDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        if self.request.method == 'GET':
            return [AllowAny()]
        return super().get_permissions()
    
    def delete(self, request, review_id):
        rating = get_object_or_404(Rating, pk=review_id)
        if rating.user != request.user:
            return Response({'error': 'У вас нет доступа для удаления'}, status=403)
        rating.delete()
        return Response({'message': 'Успешно удалено'}, status=200)


class BranchView(APIView):
    permission_classes = [IsAuthenticated, BusinessOnly]

    def get_permissions(self):
        if self.request.method == 'GET':
            return [AllowAny()]
        return super().get_permissions()
    
    def get(self, request, pk):
        carwash = get_object_or_404(Carwash, pk=pk)

        branches = Branch.objects.filter(carwash=carwash)

        if active := request.data.get('active', True):
            if active: branches = branches.filter(is_active=active)
            else: pass

        if bodytypes := request.data.get('bodytypes', None):
            branches = branches.filter(bodytypes__in=bodytypes)

        serializer = BranchSerializer(branches, many=True)
        return Response(serializer.data, status=200)
    
    def post(self, request, pk):
        carwash = get_object_or_404(Carwash, pk=pk)
        if request.user != carwash.user:
            return Response({'error': 'У вас нет доступа для добавления'}, status=403)
        serializer = BranchSerializer(data=request.data, context={'carwash':carwash})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)
    
    
class BranchDetailView(APIView):
    permission_classes = [IsAuthenticated, BusinessOnly]
    
    def delete(self, request, pk):
        branch = get_object_or_404(Branch, pk=pk)
        if request.user != branch.carwash.user:
            return Response({'error': 'У вас нет доступа для удаления'}, status=403)
        branch.delete()
        return Response({'message': 'Успешно удалено'}, status=200)
    