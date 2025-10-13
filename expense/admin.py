from django.contrib import admin
from .models import Expense, Expense_category

# Register your models here.
admin.site.register(Expense)  # Register your expense-related models here
admin.site.register(Expense_category)  # Register your expense category models here