from django.urls import path

from . import views


app_name='suppliers'

urlpatterns = [
    path('', views.SuppliersListView.as_view(), name='list'),
    path('create/sourcing/', views.SuppliersSourceCreateView.as_view(), name='create_by_sourcing'),
    path('create/sales/', views.SuppliersSalesCreateView.as_view(), name='create_by_sales'),
    path('create/<int:pk>/price/', views.SuppliereNewPriceCreateView.as_view(), name='add_price_by_sourcing'),
    path('edit/<int:pk>/', views.SupplierUpdateView.as_view(), name='update'),
    path('delete/<int:pk>/', views.SupplierDeleteView.as_view(), name='delete'),  
]
