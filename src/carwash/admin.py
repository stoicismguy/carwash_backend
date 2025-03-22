from django.contrib import admin
from .models import Carwash, Rating, Branch


class CarwashAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'name', 'phone_number', 'email', 'rating', 'is_active', 'created_at')


class RatingAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'branch', 'rating_value', 'created_at')


class BranchAdmin(admin.ModelAdmin):
    list_display = ('id', 'carwash', 'address', 'created_at')

admin.site.register(Carwash, CarwashAdmin)
admin.site.register(Rating, RatingAdmin)
admin.site.register(Branch, BranchAdmin)
