from django.urls import path

from . import views 

app_name = 'dash'

urlpatterns = [
    path('main_dash/', views.main_dash, name='main_dash'),
    path('summary/', views.summary_dash, name ='summary'),
    path('mortality/',views.mortality, name ='mortality'),
    # path('summary-chart',views.summary_chart, name ='summary-chart'),
]