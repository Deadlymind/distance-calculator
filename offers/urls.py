from django.urls import path

from . import views

app_name='offers'

urlpatterns = [
    # path('visual-maps/', views.OffersVisualMapView.as_view(), name='map_visuals'),
    path('<int:pk>/', views.OfferDetailView.as_view(), name="detail"),
]
