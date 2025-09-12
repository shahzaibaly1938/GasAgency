from django.urls import path
from . import views

urlpatterns = [
    path('', views.sell_view, name='sell'), 
    path('sell-create/', views.sell_create_view, name='sell_create'),
    path('details/<int:sell_id>/', views.sell_view_detail, name='sell_view'), 
    path('edit/<int:sell_id>/', views.sell_edit_view, name='sell_edit'),
    path('delete/<int:sell_id>/', views.sell_delete_view, name='sell_delete'),
]