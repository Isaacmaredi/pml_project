from django.urls import path
from .views import (ProfileListView, 
                    CommitteeListView, 
                    ProfileCertView, 
                    MyProfileView,
                    profile_update,pdfcert_view
                    )
from . import views 

app_name = 'pmlprofile'

urlpatterns =[
    # path('member_list/',views.member_list_view, name='member_list'),
    path('beneficiaries/',views.BeneficiaryList.as_view(), name= 'beneficiaries'),
    path('profiles/', views.ProfileListView.as_view(), name = 'profiles'),
    path('profile_detail/<int:pk>/',views.ProfileDetails.as_view(), name='profile_detail'),
    path('my_profile/<int:pk>/',views.MyProfileView.as_view(), name='my_profile'),
    path('my_profile/certificate/',views.ProfileCertView.as_view(), name='certificate'),
    path('my_profile/pdf_cert/',views.pdfcert_view, name='pdf_cert'),
    # path('profile/add/', views.ProfileCreate.as_view(), name='profile_create'),
    path('profile_update/', views.profile_update, name='profile_update'),
    path('committees/', views.CommitteeListView.as_view(), name = 'committees'),
    path('committees/<int:pk>/', views.CommitteeDetail.as_view(), name = 'committee_detail'),
    path('committee_create/', views.IncumbentCreateView.as_view(), name='committee_create'),
    path('committee_update/<int:pk>/', views.IncumbentUpdateView.as_view(), name='committee_update')
    # path('committee_update/')
]

