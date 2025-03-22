from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
import re

class UserManager(BaseUserManager):    
    def create_user(self, phone_number, password=None, **extra_fields):
        if not phone_number:
            raise ValueError("Номер телефона обязателен")
        if not password:
            raise ValueError("Пароль обязателен")
        user = self.model(phone_number=phone_number, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone_number, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(phone_number, password, **extra_fields)

class User(AbstractBaseUser):
    USER_TYPE_CHOICES = (
        ('user', 'Водитель'),
        ('business', 'Предприятие'),
    )

    # Валидатор для номера телефона (11 символов, только цифры)
    phone_regex = RegexValidator(
        regex=r'^\d{11}$',
        message="Номер телефона должен быть 11 цифр, например: 79001234567"
    )
    
    phone_number = models.CharField(
        max_length=11,
        unique=True,
        validators=[phone_regex],
        verbose_name="Номер телефона"
    )
    
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES)  # Роль
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    name = models.CharField(max_length=150, blank=False, null=False)  # Имя водилы или предприятия

    objects = UserManager()

    USERNAME_FIELD = 'phone_number'  # Теперь логин — это номер телефона
    REQUIRED_FIELDS = ['user_type']  # Для createsuperuser

    # def __str__(self):
    #     return self.phone_number

    def has_perm(self, perm, obj=None):
        return self.is_superuser

    def has_module_perms(self, app_label):
        return self.is_superuser