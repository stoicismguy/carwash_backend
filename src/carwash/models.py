from django.db import models
from users.models import User
from services.models import Bodytype
from django.core.validators import RegexValidator, MinValueValidator, MaxValueValidator

class Carwash(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='carwashes')
    name = models.CharField(max_length=100, unique=True)
    phone_number = models.CharField(
        max_length=11,
        validators=[
            RegexValidator(
                regex=r'^\d{11}$',
                message='Номер телефона должен содержать 11 цифр.'
            ),
        ]
    )
    description = models.TextField(blank=True, null=True, max_length=500)
    email = models.EmailField(blank=True, null=True)
    rating = models.DecimalField(
        max_digits=2,
        default=0.0,
        decimal_places=1,
        blank=True, null=True,
        validators=[
            MinValueValidator(1, message="Рейтинг не может быть меньше 1"),
            MaxValueValidator(5, message="Рейтинг не может быть больше 5"),
        ]
    )
    is_active = models.BooleanField(default=True)
    logo = models.URLField(blank=True, null=True)
    website = models.URLField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    # def update_rating(self):
    #     avg_rating = self.received_ratings.aggregate(models.Avg('rating_value'))['rating_value__avg']
    #     self.rating = round(avg_rating, 1) if avg_rating else 0.0
    #     self.save(update_fields=['rating'])

    
    def __str__(self):
        return f"{self.name} - {self.phone_number}"


    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Автомойка'
        verbose_name_plural = 'Автомойки'


class Branch(models.Model):
    carwash = models.ForeignKey(Carwash, on_delete=models.CASCADE, related_name='branches')
    address = models.CharField(max_length=255)
    name = models.CharField(max_length=100, blank=True, null=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    phone_number = models.CharField(
        max_length=11,
        validators=[
            RegexValidator(
                regex=r'^\d{11}$',
                message='Номер телефона должен содержать 11 цифр.'
            ),
        ]
    )
    is_active = models.BooleanField(default=True)
    opening_time = models.TimeField()
    closing_time = models.TimeField()
    bodytypes = models.ManyToManyField(Bodytype, blank=False, related_name='branch_bodytypes')
    rating = models.DecimalField(
        max_digits=2,
        default=0.0,
        decimal_places=1,
        blank=True, null=True,
        validators=[
            MinValueValidator(1, message="Рейтинг не может быть меньше 1"),
            MaxValueValidator(5, message="Рейтинг не может быть больше 5"),
        ]
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Филиал'
        verbose_name_plural = 'Филиалы'

class Rating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ratings_from')
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, related_name='received_ratings')
    description = models.TextField(blank=True, null=True)
    rating_value = models.DecimalField(
        max_digits=2,
        decimal_places=1,
        validators=[
            MinValueValidator(1, message="Рейтинг не может быть меньше 1"),
            MaxValueValidator(5, message="Рейтинг не может быть больше 5"),
        ]
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Рейтинг'
        verbose_name_plural = 'Рейтинги'
        constraints = [
            models.UniqueConstraint(fields=['user', 'branch'], name='unique_rating')
        ]