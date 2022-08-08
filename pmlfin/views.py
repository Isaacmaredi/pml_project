from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView

from django.contrib.auth.mixins import LoginRequiredMixin
from datetime import datetime, date
from django.urls import reverse, reverse_lazy
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from collections import Counter

import pandas as pd 
import numpy as np
import calendar
import json
from django.http import JsonResponse

from .models import MemberAccount, Cashflow, Company, Share, Wealth
from pmlprofile.models import Profile

# Member  accounts list
@login_required
def member_accounts(request):
    
    first_rec = MemberAccount.objects.all()[0]

    max_date = MemberAccount.objects.latest("date").date
    latest_accounts = MemberAccount.objects.filter(date=max_date)   
    context ={
        'latest_accounts': latest_accounts,
        'first_rec': first_rec,
    }
    
    return render(request, 'pmlfin/member-accounts.html', context)

# Member individual acconts
class AccountDetail(LoginRequiredMixin, DetailView):
    context_object_name = 'member_account'
    model = Profile
    template_name = 'pmlfin/account-detail.html'
    
    def get_object(self):
        return self.model.objects.get(pk=self.request.user.pk)
    
    def get_context_data(self, *args, **kwargs):    
        context = super(AccountDetail, self).get_context_data(*args, **kwargs)
        context['today'] = date.today()
        return context  

class AccountDetailPrint(LoginRequiredMixin, DetailView):
    context_object_name = 'member_account'
    model = Profile
    template_name = 'pmlfin/account-print.html'
    
    def get_object(self):
        return self.model.objects.get(pk=self.request.user.pk)
    
    def get_context_data(self, *args, **kwargs):    
        context = super(AccountDetailPrint, self).get_context_data(*args, **kwargs)
        context['today'] = date.today()
        return context  
    
# Monthly cashflow analysis
@login_required
def cashflow(request):
    cash_qs = Cashflow.objects.order_by('date')
    cash_qs1 = cash_qs.values('date','opening_bank_bal','expenses','income','closing_bank_bal')
    cash_df = pd.DataFrame.from_records(cash_qs1)

    cash_df['year'] = pd.DatetimeIndex(cash_df['date']).year
    cash_df['month_int'] =pd.DatetimeIndex(cash_df['date']).month
    cash_df['month'] = cash_df['month_int'].apply(lambda x: calendar.month_abbr[x])
    cash_df['cash'] = cash_df['closing_bank_bal'].astype(float)
    cash_df['expenses'] = cash_df['expenses'].astype(float)
    cash_df['income'] = cash_df['income'].astype(float)
    cash_df['month_year'] = cash_df['month'] + ' ' + cash_df['year'].astype(str)  
    mean_closing_bal = cash_df['closing_bank_bal'].mean()
    max_closing_bal = cash_df['closing_bank_bal'].max()
    min_closing_bal = cash_df['closing_bank_bal'].min()
    
    mean_expenses = cash_df['expenses'].mean()
    max_expenses = cash_df['expenses'].max()
    min_expenses = cash_df['expenses'].min()
    
    mean_income = cash_df['income'].mean()
    max_income = cash_df['income'].max()
    min_income = cash_df['income'].min()
    
    max_month = cash_df.loc[cash_df['closing_bank_bal'] == max_closing_bal, 'month_year'].item()
    
    max_month_income = cash_df.loc[cash_df['income'] == max_income, 'month_year'].item()
    max_month_expenses = cash_df.loc[cash_df['expenses'] == max_expenses, 'month_year'].item()
    
    
    min_month = cash_df.loc[cash_df['closing_bank_bal'] == min_closing_bal, 'month_year'].item()
    
    min_month_income = cash_df.loc[cash_df['income'] == min_income, 'month_year'].item()
    min_month_expenses = cash_df.loc[cash_df['expenses'] == min_expenses, 'month_year'].iloc[0]
    
    date_list = list(cash_df['month_year'])[-12:]
    date_list2 = list(cash_df['month_year'])[-12:]
    
    date_range = (date_list[0], date_list[-1])
    # print(date_list)
    cash_list = list(cash_df['cash'])[-12:]
    
    date_from = date_range[0]
    date_to = date_range[1]
    
    expenses_list = list(cash_df['expenses'])[-12:]
    income_list = list(cash_df['income'])[-12:]
    
    context={
        'cash_qs': cash_qs,
        'date_list': date_list,
        'cash_list': cash_list,
        'date_list2': date_list2,
        'income_list': income_list,
        'expenses_list': expenses_list,
        'mean_closing_bal': mean_closing_bal,
        'max_closing_bal': max_closing_bal,
        'min_closing_bal': min_closing_bal,
        'date_from': date_from,
        'date_to': date_to,
        'min_month': min_month,
        'max_month': max_month,
        'mean_expenses': mean_expenses,
        'max_expenses': max_expenses,
        'min_expenses': min_expenses,
        'mean_income': mean_income,
        'max_income': max_income,
        'min_income': min_income,
        'max_month_income': max_month_income,
        'max_month_expenses': max_month_expenses,
        'min_month_income': min_month_income,
        'min_month_expenses': min_month_expenses,
    }
    
    return render(request, 'pmlfin/cash-balance.html',context)

# Shares investment  analysis
def shares_view(request):
    qs_co = Company.objects.all()
    qs_co1 = qs_co.values('logo','name','trading_name', 'purchase_date',
                            'num_shares','purchase_price','purchase_value')
    
    co_df = pd.DataFrame.from_records(qs_co1)
    co_df['pur_price'] = co_df['purchase_value'].astype(float)


    name_list = list(co_df['name'])
    trade_name_list = list(co_df['trading_name'])
    purchase_value_list = list(co_df['pur_price'])
    num_shares_list = list(co_df['num_shares'])
    total_purchase_value = co_df['pur_price'].sum()
    share_qs = Share.objects.all()
    qs = share_qs.values('date','company','current_share_price','current_value')
    
    share_df = pd.DataFrame.from_records(qs)
    share_df['year'] = pd.DatetimeIndex(share_df['date']).year
    share_df['int_month'] = pd.DatetimeIndex(share_df['date']).month
    share_df['month'] = share_df['int_month'].apply(lambda x: calendar.month_abbr[x])
    share_df['month_year'] = share_df['month'] + '-' + share_df['year'].astype(str)
    
    share_df['curr_value'] = share_df['current_value'].astype(float)
    
    share_labels = share_df['month_year'].unique().tolist()
    
    mtn_df = share_df.loc[share_df['company'] == 1]
    mtn_values = list(mtn_df['curr_value'])[-12]
    
    sol_df = share_df.loc[share_df['company'] == 2]
    sol_values = list(sol_df['curr_value'])[-12]
    
    solbe_df = share_df.loc[share_df['company'] == 3]
    solbe_values = list(solbe_df['curr_value'])[-12]
    
    telkom_df = share_df.loc[share_df['company'] == 4]
    telkom_values = list(telkom_df['curr_value'])[-12]
    
    vod_df = share_df.loc[share_df['company'] == 5]
    vod_values = list(vod_df['curr_value'])[-12]

    phuthuma_df = share_df.loc[share_df['company'] == 6]
    phuthuma_values = list(phuthuma_df['curr_value'])[-12]

    yebo_df = share_df.loc[share_df['company'] == 7]
    yebo_values = list(yebo_df['curr_value'])[-12]

    latest_date = Share.objects.latest("date").date
    latest_share = Share.objects.filter(date=latest_date) 
    # df = pd.DataFrame.from_records(list(latest_share.values()))
    # print(df)
    latest_qs = latest_share.values('company','date','current_share_price','current_value')
    latest_df = pd.DataFrame.from_records(latest_qs)
    
    latest_df['curr_value'] = latest_df['current_value'].astype(float)
    total_share_value = latest_df['curr_value'].sum() 

    current_value_list = list(latest_df['curr_value'])[-12]
    
    context = {
        'qs_co': qs_co,
        'trade_name_list': trade_name_list,
        'purchase_value_list': purchase_value_list,
        'total_purchase_value': total_purchase_value,
        'current_value_list': current_value_list,
        'total_share_value': total_share_value,
        'mtn_values': mtn_values,
        'sol_values': sol_values,
        'solbe_values': solbe_values,
        'telkom_values': telkom_values,
        'vod_values': vod_values,
        'phuthuma_values': phuthuma_values,
        'yebo_values': yebo_values,
        'share_labels': share_labels,
    }
    
    return render(request, 'pmlfin/shares.html', context)

# Net Wealth analysis 
def net_wealth(request):
    qs = Wealth.objects.all()
    qs1 = qs.values('date','closing_cash_balance','notice_acc_balance',
                    'monthly_shares_total','total_net_wealth')
    
    wealth_df = pd.DataFrame.from_records(qs1)

    wealth_df['latest_date'] = wealth_df['date'].astype(str)
    wealth_df['bank_bal'] = wealth_df['closing_cash_balance'].astype(float)
    wealth_df['notice_bal'] = wealth_df['notice_acc_balance'].astype(float)
    wealth_df['shares_total'] = wealth_df['monthly_shares_total'].astype(float)
    wealth_df['tot_net_wealth'] = wealth_df['total_net_wealth'].astype(float)
    
    wealth_df['year'] = pd.DatetimeIndex(wealth_df['date']).year
    wealth_df['month_int'] =pd.DatetimeIndex(wealth_df['date']).month
    wealth_df['month'] = wealth_df['month_int'].apply(lambda x: calendar.month_abbr[x])  
    wealth_df['month_year'] = wealth_df['month'] + '-' + wealth_df['year'].astype(str)
    
    bank_bal_list = list(wealth_df['bank_bal'])[-6:]
    notice_bal_list = list(wealth_df['notice_bal'])[-6:]
    shares_total_list = list(wealth_df['shares_total'])[-6:]
    net_wealth_list = list(wealth_df['tot_net_wealth'])[-6:]
    date_list = list(wealth_df['latest_date'])[-6:]
    wealth_date_list = list(wealth_df['month_year'])[-6:]
    wealth_date_range = (wealth_date_list[0], wealth_date_list[-1])
    wealth_date_from = wealth_date_range[0]
    wealth_date_to = wealth_date_range[-1]
    
    net_wealth_average = wealth_df['tot_net_wealth'].mean().astype(float)
    net_wealth_high = wealth_df['tot_net_wealth'].max().astype(float)
    net_wealth_low = wealth_df['tot_net_wealth'].min().astype(float)
    
    highest_month = wealth_df.loc[wealth_df['tot_net_wealth'] == net_wealth_high, 'month_year'].item()
    lowest_month = wealth_df.loc[wealth_df['tot_net_wealth'] == net_wealth_low, 'month_year'].item()
    
    latest_date = Wealth.objects.latest('date').date
    latest_wealth = Wealth.objects.filter(date = latest_date)
    latest_qs = latest_wealth.values('date','closing_cash_balance','notice_acc_balance',
                    'monthly_shares_total')
    
    latest_wealth_df = pd.DataFrame.from_records(latest_qs)
    
    
    latest_wealth_df['latest_cash_bal'] = latest_wealth_df['closing_cash_balance'].astype(float)
    latest_wealth_df['latest_notice_bal']= latest_wealth_df['notice_acc_balance'].astype(float)
    latest_wealth_df['latest_share_total']= latest_wealth_df['monthly_shares_total'].astype(float)

    latest_wealth_df = latest_wealth_df.drop(['date','closing_cash_balance', 'notice_acc_balance','monthly_shares_total'], axis=1)
    # print(latest_wealth_df)
    latest_wealth_df = latest_wealth_df.transpose()
    latest_wealth_df.rename(columns={0:'latest_value'}, inplace=True)
    # print(latest_wealth_df)
    latest_net_wealth = latest_wealth_df['latest_value'].sum()  
    
    latest_wealth_labels = ['Latest Cash Bal','Latest Notice Bal','Latest Shares Value']
    latest_wealth_values = list(latest_wealth_df['latest_value'])

    print('*'*30)
    # print(date_list)
    # print('*'*30)
    # print(net_wealth_list)
    # print(net_wealth_average)
    # print(date_range)
    # print(date_from)
    # print(date_to)

    test_wealth = 'Testing Wealth Analysis'
    context = {
        'test_wealth': test_wealth,
        'wealth_date_list': wealth_date_list,
        'bank_bal_list': bank_bal_list,
        'notice_bal_list': notice_bal_list,
        'shares_total_list': shares_total_list,
        'net_wealth_list': net_wealth_list,
        'latest_net_wealth': latest_net_wealth,
        'latest_date': latest_date,
        'latest_wealth_labels': latest_wealth_labels,
        'latest_wealth_values': latest_wealth_values,
        'net_wealth_average': net_wealth_average,
        'wealth_date_from': wealth_date_from,
        'wealth_date_to': wealth_date_to,
        'net_wealth_high': net_wealth_high,
        'net_wealth_low': net_wealth_low,
        'highest_month': highest_month,
        'lowest_month': lowest_month,
        }
    return render(request, 'pmlfin/wealth.html',context)
    
    