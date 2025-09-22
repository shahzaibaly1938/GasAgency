from django.urls import path
from . import views

urlpatterns = [
    path('', views.customer_view, name='customer'),
    path('create/', views.create_customer_view, name='create_customer'),
    path('update/<int:id>/', views.update_customer_view, name='update_customer'),
    path('detail/<int:id>/', views.customer_detail_view, name='customer_view'),
    path('delete/<int:id>/', views.delete_customer_view, name='customer_delete'),
]