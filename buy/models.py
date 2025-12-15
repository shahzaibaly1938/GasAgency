from django.db import models
from vendor.models import Vendor
from datetime import datetime
# Create your models here.


class AddStock(models.Model):
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    no_domestic_cylinder = models.PositiveIntegerField(default=0)
    domestic_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    no_commercial_cylinder = models.PositiveIntegerField(default=0)
    commercial_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    return_domestic_cylinder = models.PositiveIntegerField(default=0)
    return_commercial_cylinder = models.PositiveIntegerField(default=0)
    total_amount = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)
    date = models.DateTimeField(default=datetime.now)

    def __str__(self):
        return f"Stock from {self.vendor.name} - Total: {self.total_amount}"
    
class Stock(models.Model):
    no_domestic_cylinder = models.PositiveIntegerField(default=0)
    no_commercial_cylinder = models.PositiveIntegerField(default=0)


    def __str__(self):
        return f"Stock - Domestic: {self.no_domestic_cylinder}, Commercial: {self.no_commercial_cylinder}"
    



