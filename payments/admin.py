from django.contrib import admin
from .models import CustomerPayment, DuePayment

# Register your models here.
admin.site.register(CustomerPayment)
admin.site.register(DuePayment)