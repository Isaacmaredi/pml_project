from django.shortcuts import render
from django.db.models import Count
from datetime import datetime, date
from collections import Counter
from django.contrib.auth.decorators import login_required

import pandas as pd 
import numpy as np
import json
from django.http import JsonResponse
# Create your views here.

from pmlprofile.models import Profile, Beneficiary

#Chartjs plots
@login_required
def main_dash(request):
    mem_qs = Profile.objects.all()
    mem_qs = mem_qs.values('shortname','birth_date','status')
    member_df = pd.DataFrame.from_records(mem_qs)
    
    member_status = member_df['status'].value_counts().rename_axis('status').reset_index(name ='counts')    
    status_list = member_status['status'].to_list()
    counts = member_status['counts'].to_list()
    total = member_df.shape[0]
    
    print(status_list)
    print(counts)

    ben_qs = Beneficiary.objects.all()
    ben_qs = ben_qs.values('name','beneficiary_status')
    ben_df = pd.DataFrame.from_records(ben_qs)
    
    ben_status = ben_df['beneficiary_status'].value_counts().rename_axis('beneficiary_status').reset_index(name='ben_counts')

    ben_status_list = ben_status['beneficiary_status'].to_list()
    ben_counts = ben_status['ben_counts'].to_list()
    ben_total  = ben_df.shape[0]
    
    # member_csv = member_df.to_csv(r'member.csv')
    # beneficiary_csv = ben_df.to_csv(r'beneficiary.csv')
    context = {
        'status_list': status_list,
        'counts':counts,
        'total': total,
        'ben_status_list': ben_status_list,
        'ben_counts': ben_counts,
        'ben_total': ben_total,
    }

    return render(request, 'dash/main-dash.html', context)

@login_required
def summary_dash(request):
    

    qs = Profile.objects.all().values('status').annotate(total=Count('status'))
    total_members = Profile.objects.all().count()
    
    qs = Profile.objects.all()
    q = qs.values('shortname','status')
    member_status_df = pd.DataFrame.from_records(q)
    
    member_status = member_status_df['status'].value_counts().rename_axis('status').reset_index(name='status_count')
    
    member_status_list = member_status['status'].to_list()
    status_count = member_status['status_count'].to_list()
    
    ben_qs = Beneficiary.objects.all()
    ben_qs = ben_qs.values('name','beneficiary_status')
    ben_df = pd.DataFrame.from_records(ben_qs)
    
    ben_status = ben_df['beneficiary_status'].value_counts().rename_axis('beneficiary_status').reset_index(name='ben_counts')
    ben_status_list = ben_status['beneficiary_status'].to_list()
    ben_counts = ben_status['ben_counts'].to_list()
    ben_total  = ben_df.shape[0]
    # except:
        # raise KeyError ('No beneficiaries in database')
    # Members Queryset to pandas and csv     
    qs = Profile.objects.all()
    q = qs.values('shortname','birth_date','status')
    df_member = pd.DataFrame.from_records(q)
    # member_csv = df_member.to_csv(r'member.csv')

    # Beneficiary Quesryset to pandas csv 
    qs1 = Beneficiary.objects.all()
    q1 = qs1.values('name', 'birth_date', 'beneficiary_type','beneficiary_status')
    df_ben = pd.DataFrame.from_records(q1)
    
    df_member = df_member.drop(df_member[df_member.status =="Deceased"].index)
    df_member = df_member.drop(df_member[df_member.status =="Terminated"].index)
    active_member_tot = len(df_member)
    
    df_ben = df_ben.drop(df_ben[df_ben.beneficiary_status =="Deceased"].index)
    df_ben = df_ben.drop(df_ben[df_ben.beneficiary_status =="Inactive"].index)
    active_ben_tot = len(df_ben)
    
    def age(born):
        born = str(born)
        born = datetime.strptime(born, '%Y-%m-%d').date()
        today = date.today()
        return today.year - born.year  
    
    df_member['member_age'] = df_member['birth_date'].apply(age)
    df_ben['ben_age'] = df_ben['birth_date'].apply(age)
    
    member_summary  = df_member['member_age'].describe()
    ben_summary  = df_ben['ben_age'].describe()
    
    conditions = [
        (df_member['member_age'] < 50),
        (df_member['member_age'] < 55),
        (df_member['member_age'] < 60),
        (df_member['member_age'] < 65),
        (df_member['member_age'] < 70),
        (df_member['member_age'] < 80),
        (df_member['member_age'] >79),
        ]

    values = ['0 to 49 years', '50 to 54 years',
            '55 to 59 years','60 to 64 years', '65 to 69 years',
            '70 to 79 years','80 years and older',
            ]

    df_member['member_age_group'] = np.select(conditions, values)

    member_age_group_list = list(df_member['member_age_group'])
    member_age_group_list.sort()
    member_age_group_dict = dict(Counter(member_age_group_list))

    member_age_group_keys = member_age_group_dict.keys()
    member_age_group_values = member_age_group_dict.values()
    
    member_age_group_labels= []
    member_age_group_data = []
    
    for x in member_age_group_keys:
        member_age_group_labels.append(x)
    
    for y in member_age_group_values:
            member_age_group_data.append(y)
            
    # Beneficiary Age Groups are
    conditions = [
        (df_ben['ben_age'] < 18),
        (df_ben['ben_age'] < 36),
        (df_ben['ben_age'] < 50),
        (df_ben['ben_age'] < 60),
        (df_ben['ben_age'] < 70),
        (df_ben['ben_age'] < 80),
        (df_ben['ben_age'] < 100),
        (df_ben['ben_age'] > 99),
        ]

    values = ['0 to 17 years', '18 to 35 years',
            '36 to 49 years','50 to 59 years', '60 to 69 years',
            '70 to 79 years','80 to 99 years','Centenarians',
            ]

    df_ben['ben_age_group'] = np.select(conditions, values)

    ben_age_group_list = list(df_ben['ben_age_group'])
    ben_age_group_list.sort()
    ben_age_group_dict = dict(Counter(ben_age_group_list))

    
    ben_age_group_keys = ben_age_group_dict.keys()
    ben_age_group_values = ben_age_group_dict.values()
    
    ben_age_group_labels= []
    ben_age_group_data = []
    
    for x in ben_age_group_keys:
        ben_age_group_labels.append(x)
    
    for y in ben_age_group_values:
            ben_age_group_data.append(y)
            
    # Beneiciaries by type and status   
    ben_qs = Beneficiary.objects.all()
    ben_qs = ben_qs.values('beneficiary_type', 'beneficiary_status')
    ben_df_stats = pd.DataFrame.from_records(ben_qs)
    
    ben_stat = ben_df_stats.groupby(ben_df_stats['beneficiary_type'])
    
    ben_stats = ben_stat['beneficiary_status'].value_counts().sort_index(ascending=True)
    ben_stats_df = pd.Series.to_frame(ben_stats, name='counts')
    
    ben_type_pivot = ben_stats_df.pivot_table(index='beneficiary_type', columns= 'beneficiary_status')
    ben_type_pivot.columns = ben_type_pivot.columns.droplevel(0)
    ben_type_pivot.columns.name = None
    ben_type_df = ben_type_pivot.reset_index().rename_axis(None, axis=1)
    
    ben_type_df = ben_type_df.replace(np.nan,0)
    
    df_ben_type = df_ben.groupby(df_ben['ben_age_group'])
    df_ben_types = df_ben_type['beneficiary_type'].value_counts().sort_index(ascending=True)
    df_ben_group = pd.Series.to_frame(df_ben_types, name= 'type_counts')
    
    df_ben_pivot = df_ben_group.pivot_table(index = 'ben_age_group', columns ='beneficiary_type')
    df_ben_pivot.columns = df_ben_pivot.columns.droplevel(0)
    df_ben_pivot.columns.name = None
    df_ben_age_type =  df_ben_pivot.reset_index().rename_axis(None, axis = 1)
    df_ben_age_type = df_ben_age_type.replace(np.nan,0)
    
    ben_type_list = list(ben_type_df['beneficiary_type'])
    ben_age_type_list = list(df_ben_age_type['ben_age_group'])
    
    ben_child, ben_father, ben_fil, ben_mother, ben_mil, ben_proxy, ben_spouse = [],[],[],[],[],[],[]
    
    ben_active = []
    ben_article20 = []
    ben_deceased = []
    ben_inactive = []
    try:
        ben_type_active = dict(ben_type_df['Active']).values()
    except KeyError:
        ben_type_active = 0
    try:
        ben_type_article20 = dict(ben_type_df['Article 20.3']).values()['ben_type_article20']
        for x in ben_type_article20:
            ben_article20.append(x)
    except KeyError:
        ben_type_article20 = 0
    try:
        ben_type_deceased = dict(ben_type_df['Deceased']).values()
        for y in ben_type_deceased:
            ben_deceased.append(y)
    except KeyError:
        ben_type_deceased = 0
    try:
        ben_type_inactive = dict(ben_type_df['Inactive']).values()
        for z in ben_type_inactive:
            ben_inactive.append(z)
    except KeyError:
        ben_type_deceased = 0
    try:
        ben_type_child = dict(df_ben_age_type['Child']).values()
        for child in ben_type_child:
            ben_child.append(child)
    except KeyError:
        ben_type_child = 0 
    try:
        ben_type_father = dict(df_ben_age_type['Father']).values()
        for father in ben_type_father:
            ben_father.append(father)
    except KeyError:
        ben_type_father = 0
    try:
        ben_type_fil = dict(df_ben_age_type['Father-in-Law']).values()
        for f in ben_type_fil:
            ben_fil.append(f)
    except KeyError:
        ben_type_fil = 0
    try:
        ben_type_mother = dict(df_ben_age_type['Mother']).values()
        for mother in ben_type_mother:
            ben_mother.append(mother)
    except KeyError:
        ben_type_mother = 0
    try:
        ben_type_mil = dict(df_ben_age_type['Mother-in-Law']).values()
        for m in ben_type_mil:
            ben_mil.append(m)
    except KeyError:
        ben_type_mil = 0
    try:
        ben_type_proxy = dict(df_ben_age_type['Parent Proxy']).values()
        for p in ben_type_proxy:
            ben_proxy.append(p)
    except KeyError:
        ben_type_proxy = 0
    try:
        ben_type_spouse = dict(df_ben_age_type['Spouse']).values()
        for s in ben_type_spouse:
            ben_spouse.append(s)
    except KeyError:
        ben_type_spouse = 0
    
    for i in ben_type_active:
        ben_active.append(i)

    context = {
        'member_status_list': member_status_list,
        'status_count': status_count,
        'total_members': total_members,
        'ben_status_list': ben_status_list,
        'ben_counts':ben_counts,
        'ben_total': ben_total,
        'member_age_group_labels': member_age_group_labels,
        'member_age_group_data': member_age_group_data,
        'ben_age_group_labels': ben_age_group_labels,
        'ben_age_group_data': ben_age_group_data, 
        'active_member_tot': active_member_tot,
        'active_ben_tot': active_ben_tot, 
        'ben_type_list': ben_type_list,
        'ben_active': ben_active,
        'ben_article20': ben_article20,
        'ben_deceased': ben_deceased,
        'ben_inactive': ben_inactive,  
        'ben_age_type_list': ben_age_type_list,
        'ben_child': ben_child,
        'ben_father': ben_father,
        'ben_fil': ben_fil,
        'ben_mother': ben_mother,
        'ben_mil':ben_mil,
        'ben_proxy': ben_proxy,
        'ben_spouse': ben_spouse,
    }
    
    return render(request, 'dash/summary.html',context)

@login_required
def mortality(request):
    member_mortality = Profile.objects.filter(status='Deceased')
    qm = member_mortality.values('shortname','birth_date','status','status_date')
    member_mortality_df = pd.DataFrame.from_records(qm)
    
    member_mortality_df['year'] = pd. DatetimeIndex(member_mortality_df['status_date']).year
    
    death_year_df = member_mortality_df['year'].value_counts().rename_axis('year').reset_index(name='death_count').sort_index()
    
    death_year_df = death_year_df.sort_values(by='year')
    
    year_list = list(death_year_df['year'])
    year_death_count = list(death_year_df['death_count'])

    stats = death_year_df.describe()
    stats_df = pd.DataFrame(stats)
    
    data = pd.DataFrame(stats_df).to_html()
    
    ben_mortality = Beneficiary.objects.filter(beneficiary_status='Deceased')
    qb = ben_mortality.values('name','beneficiary_status','paid_date')
    ben_mortality_df = pd.DataFrame.from_records(qb)
    
    ben_mortality_df['year'] = pd.DatetimeIndex(ben_mortality_df['paid_date']).year
    
    ben_death_year= ben_mortality_df['year'].value_counts().rename_axis('year').reset_index(name='death_count').sort_index()

    ben_death_year = ben_death_year.sort_values(by='year')
    
    ben_year_list = list(ben_death_year['year'])
    ben_death_count = list(ben_death_year['death_count'])
    
    context = {
        'stats_df': stats_df,
        'data': data,
        'year_list':year_list,
        'year_death_count':year_death_count,
        'ben_year_list': ben_year_list,
        'ben_death_count':ben_death_count,
    }   
    
    return render(request, 'dash/mortality.html',context)
    
    