from django.urls import path
from .views import (ProfileListView, CommitteeListView, IncumbentUpdateView,
                    MyProfileView, ProfileCertView, BeneficiaryList, #MemberAccountView,
                    ProfileDetails, CommitteeDetail, IncumbentCreateView,
)                
from .views import profile_update, pdfcert_view, membercert_view

from django.contrib.auth.decorators import login_required

app_name = 'pmlprofile'

urlpatterns =[
    # path('member_list/',views.member_list_view, name='member_list'),
    path('beneficiaries/',BeneficiaryList.as_view(), name= 'beneficiaries'),
    path('profiles/',ProfileListView.as_view(), name = 'profiles'),
    path('profile_detail/<int:pk>/',ProfileDetails.as_view(), name='profile_detail'),
    path('my_profile/<int:pk>/',login_required(MyProfileView.as_view(template_name='pmlprofile/my_profile.html')), name='my_profile'),
    path('my_cert/<int:pk>/',ProfileCertView.as_view(), name='my_cert'),
    path('pdf_cert/<int:pk>',pdfcert_view, name='pdf_cert'),
    path('membercert/<int:pk>/',membercert_view, name='membercert'),
    # path('profile_dash/',profile_dash, name='profile_dash'),
    # path('ben_dash/',ben_dash, name='ben_dash'),
    # path('member_accounts/', MemberAccountView.as_view(), name='member_accounts'),
    
    # path('pdf_certificate/', views.pdf_certificate, name='pdf-certificate'),
    # path('my_cert/pdf_cert/<int:pk>/',views.pdfcert_view, name='pdf_cert'),
    # path('profile/add/', views.ProfileCreate.as_view(), name='profile_create'),
    path('profile_update/',profile_update, name='profile_update'),
    path('committees/',CommitteeListView.as_view(), name = 'committees'),
    path('committees/<int:pk>/',CommitteeDetail.as_view(), name = 'committee_detail'),
    path('committee_create/', IncumbentCreateView.as_view(), name='committee_create'),
    path('committee_update/<int:pk>/', IncumbentUpdateView.as_view(), name='committee_update')
    # path('committee_update/')
]

