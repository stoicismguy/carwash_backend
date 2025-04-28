from django.db import models
from django.core.validators import MinValueValidator


class ServiceGroup(models.Model):
    branch = models.ForeignKey('carwash.Branch', on_delete=models.CASCADE)
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return f"{self.branch.carwash} {self.name}"

    class Meta:
        verbose_name = 'Группа услуг'
        verbose_name_plural = 'Группы услуг'


class Service(models.Model):
    group = models.ForeignKey(ServiceGroup, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    price = models.DecimalField(max_digits=10,
                                decimal_places=2,
                                validators=[
                                    MinValueValidator(0)
                                ])
    duration = models.TimeField()

    def __str__(self):
        return f"{self.id} {self.group.branch.carwash} {self.group.name} {self.name}"
    
    class Meta:
        verbose_name = 'Услуга'
        verbose_name_plural = 'Услуги'
        

class Bodytype(models.Model):
    name = models.CharField(max_length=100, unique=True)
    image = models.URLField(null=True, blank=True)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Тип кузова'
        verbose_name_plural = 'Типы кузовов'