from django.urls import path
from . import views 

app_name = 'pmlprofile'

urlpatterns =[
    # path('member_list/',views.member_list_view, name='member_list'),
    path('beneficiaries/',views.BeneficiaryList.as_view(), name= 'beneficiaries'),
    path('profiles/', views.ProfileListView.as_view(), name = 'profiles'),
    # path('profile_create/<int:pk>',views.profile_create_view, name='profile_create'),
    path('profile_detail/<int:pk>/',views.ProfileDetails.as_view(), name='profile_detail'),
    path('profile_update/',views.profile_update, name='profile_update'),
    path('committee_create/', views.committee_create_view, name='committee_create'),
    path('committee_list/', views.committee_list_view, name='committee_list'),
    path('committee_update/<int:pk>',views.committee_update_view, name='committee_update'),
]
