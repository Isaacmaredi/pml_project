from django.urls import path
from . import views 

app_name = 'accounts'

urlpatterns =[
    path('login_view',views.login_view, name='login_view'),
    path('register',views.register, name='register'),
]
