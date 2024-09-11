from django.urls import path

from . import views


app_name='products'

urlpatterns = [
    path('', views.ProductsListView.as_view(), name='list'),
    path('create/', views.ProductsCreateView.as_view(), name='create'),
    path('update/<int:pk>/', views.ProductsUpdateView.as_view(), name='update'),
    path('delete/<int:pk>/', views.ProductsDeleteView.as_view(), name='delete'),
    path('unit/create/', views.UnitCreateView.as_view(), name='unit_create'),
]
