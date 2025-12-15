from django.db import models
from customer.models import Customer
from sell.models import Sell

# Create your models here.

class CustomerPayment(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    sell_record = models.ForeignKey(Sell, on_delete=models.CASCADE)
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateTimeField()
    payment_method = models.CharField(max_length=50, choices=[("cash", "Cash"),("bank","Bank Transfer"), ("card","Card")])
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.customer.name} - {self.amount_paid} on {self.payment_date}"



class DuePayment(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    sell_record = models.ForeignKey(Sell, on_delete=models.CASCADE)
    amount_due = models.DecimalField(max_digits=10, decimal_places=2)
    updated_date = models.DateTimeField()
    due_date = models.DateTimeField()

    def __str__(self):
        return f"{self.customer.name} - Due: {self.amount_due} by {self.due_date}"