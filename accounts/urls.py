from django.urls import path

from . import views

app_name='accounts'

urlpatterns = [
    path('login/',views.login, name='login'),
    path('logout/',views.logout, name='logout'),
    path('user_profile/',views.user_profile, name='user_profile'),

    path('',views.UserListView.as_view(), name='list'),
    path('create/',views.UserCreateView.as_view(), name='create'),

]
