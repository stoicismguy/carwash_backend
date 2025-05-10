from rest_framework.viewsets import ViewSet, ModelViewSet
from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView
from rest_framework.decorators import action, permission_classes, api_view
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from .serializers import UserSerializer, CreateUserSerializer
from .models import User

class UserViewSet(ModelViewSet):
    """Вьюсет для CRUD для пользователя (получение и т.д)"""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return User.objects.filter(id=self.request.user.id).first()
    

class UserView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response(UserSerializer(request.user).data)
    
    def patch(self, request):
        
        if phone := request.data.get('phone_number', None):
            if request.user.phone_number == phone:
                request.data.pop('phone_number')
        print(request.data)
        serializer = UserSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)
    
@api_view(["POST",])
@permission_classes([AllowAny,])
def register(request):
    serializer = CreateUserSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.create(serializer.data)
        token = RefreshToken.for_user(user)
        return Response({
            'user': UserSerializer(user).data,
            'refresh': str(token),
            'access': str(token.access_token)
        }, status=201)
    return Response(serializer.errors, status=400)



    


