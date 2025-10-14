from django.urls import path
from . import views

urlpatterns = [
    path('', views.expenses_list, name='expense'),
    path('add-expenses/', views.add_expenses, name='add_expenses'),
    path('add-expenses-category/', views.add_expenses_category, name='add_expenses_category'),
    path('expense-details/<int:id>/', views.expense_detail, name='expense_detail'),
    path('edit-expenses/<int:id>/', views.edit_expenses, name='edit_expenses'),
    path('delete-expenses/<int:id>/', views.delete_expense, name='delete_expense'),
    path('expense-categories/', views.expense_category_list, name='expense_category_list'),
    path('delete-expense-category/<int:id>/', views.delete_expense_category, name='delete_expense_category'),
    path('edit-expense-category/<int:id>/', views.edit_expense_category, name='edit_expense_category'),
]