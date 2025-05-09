from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from settings.permissions import BusinessOnly
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from django.shortcuts import get_object_or_404
from django.db.models import Sum

from carwash.models import Carwash, Branch
from .models import Service, ServiceGroup
from .serializers import ServiceGroupSerializer, ServiceSerializer


@api_view(['GET'])
@permission_classes([AllowAny])
def get_branch_services(request, pk):
    branch = get_object_or_404(Branch, pk=pk)
    groups = ServiceGroup.objects.filter(branch=branch)
    return Response(ServiceGroupSerializer(groups, many=True).data, status=200)


# class ServicesView(APIView):
#     permission_classes = [IsAuthenticated, BusinessOnly]

#     def get_permissions(self):
#         if self.request.method == 'GET':
#             return [AllowAny()]
#         return super().get_permissions()

#     def get(self, request, pk):
#         branch = get_object_or_404(Branch, pk=pk)
#         groups = ServiceGroup.objects.filter(branch=branch)
#         return Response(ServiceGroupSerializer(groups, many=True).data, status=200)


class BranchServiceGroupDetailView(APIView):
    permission_classes = [IsAuthenticated, BusinessOnly]

    def post(self, request, pk):
        branch = get_object_or_404(Branch, pk=pk)
        serializer = ServiceGroupSerializer(data=request.data, context={'branch':branch})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)
    

class ServiceGroupDetailView(APIView):
    permission_classes = [IsAuthenticated, BusinessOnly]

    def post(self, request, pk):
        group = get_object_or_404(ServiceGroup, pk=pk)
        serializer = ServiceSerializer(data=request.data, context={'group':group})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)
    
    def patch(self, request, pk):
        service = get_object_or_404(Service, pk=pk)
        serializer = ServiceSerializer(service, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.update(serializer.instance, serializer.validated_data)
            return Response(serializer.data, status=200)
        return Response(serializer.errors, status=400)
    
    
    def delete(self, request, pk):
        service = get_object_or_404(Service, pk=pk)
        service.delete()
        return Response(status=204)
    

@api_view(['POST'])
@permission_classes([AllowAny])
def get_info_services(request):
    services = request.data.get('services')
    if not services:
        return Response({'error': 'Услуги не указаны'}, status=400)
    services = Service.objects.filter(id__in=services).select_related('group').select_related('group__branch')
    branch = services.first().group.branch
    values = services.aggregate(total_price=Sum('price'), total_duration=Sum('duration'))
    return Response({
        'services': ServiceSerializer(services, many=True).data,
        'total_price': values['total_price'],
        'total_duration': str(values['total_duration']),
        'address': branch.address
        }, status=200)




