from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('api/admin/', admin.site.urls),
    path('api/users/', include('users.urls')),
    path('api/carwashes/', include('carwash.urls')),
    path('api/services/', include('services.urls')),
]
