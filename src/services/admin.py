from django.contrib import admin
from .models import ServiceGroup, Service, Bodytype


admin.site.register(ServiceGroup)
admin.site.register(Service)
admin.site.register(Bodytype)
