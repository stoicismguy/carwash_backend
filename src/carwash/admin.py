from django.contrib import admin
from .models import Carwash, Rating


class CarwashAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'name', 'phone_number', 'email', 'rating', 'is_active', 'created_at')


class RatingAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'carwash', 'rating_value', 'created_at')

admin.site.register(Carwash, CarwashAdmin)
admin.site.register(Rating, RatingAdmin)
