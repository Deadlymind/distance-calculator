from django.urls import path

from . import views

app_name='notifications'

urlpatterns = [
    path('source/', views.NotificationSourceListView.as_view(), name='source_list'),
    path('sales/', views.NotificationSalesListView.as_view(), name='sales_list')
]
