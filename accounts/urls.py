from django.urls import path
from . import views 

app_name = 'accounts'

urlpatterns =[
    path('login_view',views.login_view, name='login_view'),
    path('register',views.register, name='register'),
    path('logout', views.logout_view, name ='logout'),
    path('change_password/', views.MyPasswordChangeView.as_view(),name ='change_password'),
    path('change_password_done/', views.MyPasswordChangeDoneView.as_view(),name = 'change_password_done')
]
