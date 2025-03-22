from rest_framework.serializers import ModelSerializer
from rest_framework.exceptions import ValidationError
from .models import User

class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['phone_number', 'user_type', 'name']


class CreateUserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['phone_number', 'user_type', 'name', 'password']
        extra_kwargs = {
            'name': {'required': True}
        }

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        password = self.validate_password(validated_data['password'])
        user.set_password(password)
        user.save()
        return user
    
    def validate_password(self, value):
        if len(value) < 8:
            raise ValidationError("Пароль должен быть минимум 8 символов")
        if not any(c.isalpha() for c in value):
            raise ValidationError("Пароль должен содержать хотя бы одну букву")
        if not any(c.isdigit() for c in value):
            raise ValidationError("Пароль должен содержать хотя бы одну цифру")
        return value
