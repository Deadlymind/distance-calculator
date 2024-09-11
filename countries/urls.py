from django.urls import path

from . import views


app_name = "countries"

urlpatterns = [
    path('transportation/setup/', views.TransportationSetupView.as_view(), name='transportation_setup'),

    path('country/create/', views.CountryCreateView.as_view(), name='country_create'),
    path('country/update/<int:pk>/', views.CountryUpdateView.as_view(), name='country_update'),
    path('country/delete/<int:pk>/', views.CountryDeleteView.as_view(), name='country_delete'),

    path('region/create/<int:pk>/', views.RegionCreateView.as_view(), name='region_create'),
    path('region/delete/<int:pk>/', views.RegionDeleteView.as_view(), name='region_delete'),
    path('region/location/<int:pk>/', views.RegionLocationUpdateView.as_view(), name='region_edit_location'),

    path('region/closest/', views.ClosestRegionByCoordinatesView.as_view(), name='api_closest_region')
]
