from django.urls import path
from . import views 

app_name = 'pmlprofile'

urlpatterns =[
    path('profile_home',views.profile_home, name='profile_home'),
    path('members',views.members, name='members'),
    path('beneficiaries',views.beneficiaries, name='beneficiaries'),
    path('member_profile',views.member_profile, name='member_profile'),
]
