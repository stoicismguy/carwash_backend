from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status
from django.db import IntegrityError

def integrity_handler(exc, context):
    response = exception_handler(exc, context)

    if isinstance(exc, IntegrityError):
        return Response(
            {'error': 'Вы уже совершали данное действие!'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    return response