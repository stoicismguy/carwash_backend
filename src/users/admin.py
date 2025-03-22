from django.contrib import admin
from .models import User
# Register your models here.

class UserAdmin(admin.ModelAdmin):
    list_display = ['phone_number', 'user_type', 'name']

admin.site.register(User, UserAdmin)