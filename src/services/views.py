from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from settings.permissions import BusinessOnly
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from carwash.models import Carwash, Branch
from .models import Service, ServiceGroup
from .serializers import ServiceGroupSerializer, ServiceSerializer


class ServicesView(APIView):
    permission_classes = [IsAuthenticated, BusinessOnly]

    def get_permissions(self):
        if self.request.method == 'GET':
            return [AllowAny()]
        return super().get_permissions()

    def get(self, request, pk):
        branch = get_object_or_404(Branch, pk=pk)
        groups = ServiceGroup.objects.filter(branch=branch)
        return Response(ServiceGroupSerializer(groups, many=True).data, status=200)


    def post(self, request, pk):
        branch = get_object_or_404(Branch, pk=pk)
        serializer = ServiceSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


class ServiceDetailView(APIView):
    permission_classes = [IsAuthenticated, BusinessOnly]

    def get(self, request, pk):
        service = get_object_or_404(Service, pk=pk)
        serializer = ServiceSerializer(service)
        return Response(serializer.data, status=200)




