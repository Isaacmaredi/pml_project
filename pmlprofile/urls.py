from django.urls import path
from .views import ProfileListView, CommitteeListView, profile_update
from . import views 

app_name = 'pmlprofile'

urlpatterns =[
    # path('member_list/',views.member_list_view, name='member_list'),
    path('beneficiaries/',views.BeneficiaryList.as_view(), name= 'beneficiaries'),
    path('profiles/', views.ProfileListView.as_view(), name = 'profiles'),
    path('profile_detail/<int:pk>/',views.ProfileDetails.as_view(), name='profile_detail'),
    path('my_profile/',views.my_profile, name='my_profile'),
    # path('profile/add/', views.ProfileCreate.as_view(), name='profile_create'),
    path('profile_update/', views.profile_update, name='profile_update'),
    path('committees/', views.CommitteeListView.as_view(), name = 'committees'),
    path('committees/<int:pk>/', views.CommitteeDetail.as_view(), name = 'committee_detail'),
    path('committee_create/', views.CommitteeCreateView.as_view(), name='committee_create'),
    # path('committee_update/')
]

