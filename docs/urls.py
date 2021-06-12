from django.urls import path
from . import views

app_name = 'docs'

urlpatterns =[
    path('minutes_list/',views.minutes_list, name='minutes_list'),
    path('upload_minutes/',views.upload_minutes, name='upload_minutes'),
]