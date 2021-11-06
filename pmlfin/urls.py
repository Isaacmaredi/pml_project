from django.urls import path
from django.contrib.auth.decorators import login_required
from . import views


app_name = 'pmlfin'

urlpatterns = [
    path('member-accounts/', views.member_accounts, name='member-accounts'),
    path('cashflow/', views.cashflow, name='cashflow'),
    path('shares/', views.shares_view, name='shares'),
    path('acc_detail/<int:pk>/', views.AccountDetail.as_view(), name='acc_detail'),
    path('acc_print/<int:pk>/', views.AccountDetailPrint.as_view(), name='acc_print'),
    path('wealth/',views.net_wealth, name='wealth')
]