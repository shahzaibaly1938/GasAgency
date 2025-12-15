from django.urls import path
from . import views

urlpatterns = [
    path('', views.buy_view, name='buy'), 
    path('add-stock/', views.add_stock_view, name='add_stock'), 
]