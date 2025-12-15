from django.urls import path
from . import views

urlpatterns = [
    path('', views.vednor_list_view, name='vendor_list'),
    path('create/', views.create_vendor, name='create_vendor'),
    path('update/<int:id>/', views.update_vendor, name='update_vendor'),
    path('detail/<int:id>/', views.vendor_details, name='vendor_details'),
    path('delete/<int:id>/', views.delete_vendor, name='vendor_delete'),
]