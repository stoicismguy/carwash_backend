from rest_framework.permissions import BasePermission
from rest_framework.exceptions import PermissionDenied


class BusinessOnly(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated and request.user.user_type == 'business':
            return True
        raise PermissionDenied("Тип аккаунта должен быть Бизнес")