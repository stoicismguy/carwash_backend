from django.db import models


class Booking(models.Model):
    user = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='bookings')
    branch = models.ForeignKey('carwash.Branch', on_delete=models.CASCADE, related_name='branches')
    services = models.ManyToManyField('services.Service', blank=False, related_name='services')
    datetime = models.DateTimeField()
    status = models.CharField(max_length=20, default='pending')