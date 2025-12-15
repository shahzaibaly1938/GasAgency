from django.urls import path
from . import views

urlpatterns = [
    path('', views.payment_home, name='payments_home'),
    path('add-payment/<int:sell_id>/', views.add_payment, name='add_payment'),
    path('dues/', views.payment_dues, name='payment_dues'),
    path('process/<int:sell_id>/', views.payment_process, name='payment_process'),
]
