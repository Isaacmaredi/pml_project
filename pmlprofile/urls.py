from django.urls import path
from .views import ProfileListView, ProfileCreate, ProfileUpdate
from . import views 

app_name = 'pmlprofile'

urlpatterns =[
    # path('member_list/',views.member_list_view, name='member_list'),
    path('beneficiaries/',views.BeneficiaryList.as_view(), name= 'beneficiaries'),
    path('profiles/', views.ProfileListView.as_view(), name = 'profiles'),
    path('profile_detail/<int:pk>/',views.ProfileDetails.as_view(), name='profile_detail'),
    path('my_profile/<int:pk>/',views.MyProfile.as_view(), name='my_profile'),
    path('profile/add/', views.ProfileCreate.as_view(), name='profile_create'),
    path('profile_update/<int:pk>/', views.ProfileUpdate.as_view(), name='profile_update'),
]
