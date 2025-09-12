from django.db import models

# Create your models here.
class Customer(models.Model):
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15, unique=True)
    type = models.CharField(max_length=50, choices=[('residential', 'Residential'), ('commercial', 'Commercial')])
    address = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name