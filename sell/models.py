from django.db import models
from customer.models import Customer
from datetime import datetime

# Create your models here.
class Sell(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='sales')
    no_domestic_cylinder = models.PositiveIntegerField(default=0)
    domestic_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    no_commercial_cylinder = models.PositiveIntegerField(default=0)
    commercial_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    return_domestic_cylinder = models.PositiveIntegerField(default=0)
    return_commercial_cylinder = models.PositiveIntegerField(default=0)
    total_amount = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)
    payment_status = models.CharField(max_length=20, choices=[("paid", "Paid"), ("due", "Due") , ("partialy", "Partialy")], default="due")
    due_amount = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)
    date = models.DateTimeField(default=datetime.now)

    def __str__(self):
        return f"Sell to {self.customer.name} on {self.date}"
