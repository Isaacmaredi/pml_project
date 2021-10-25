from django.urls import path
from .import views

app_name = 'geoApp'

urlpatterns = [
    path('profile_geo/',views.profile_geo, name='profile_geo')
]