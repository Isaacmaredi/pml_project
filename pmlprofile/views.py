from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import ListView,DetailView
from datetime import datetime, date
from django.db.models import Count
                                
from django.views.generic.edit import UpdateView, CreateView
from .models import Profile, Beneficiary, Committee, Incumbent #MemberAccount
from .forms import UserUpdateForm, ProfileUpdateForm 
from django.urls import reverse, reverse_lazy

# PDF convertion
from io import BytesIO
import os
from django.conf import settings
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.contrib.staticfiles import finders

#Dashboards and graphs
from math import pi

import pandas as pd
import numpy as np

from bokeh.io import output_file, show
from bokeh.embed import components
from bokeh.models import HoverTool, ColumnDataSource
from bokeh.palettes import (Spectral6, Magma, Viridis, Plasma, 
                            Cividis, Category10, Category20, Category20b,
                            Category20c)
from bokeh.plotting import figure
from bokeh.transform import cumsum





# Beneficiaries Status Count 
@login_required
def profile_dash(request):
    actives = 0
    article20 = 0
    inactives = 0
    deceased = 0
    counts = []
    status = ['Active', 'Article 20.3', 'Inactive', 'Deceased']
    count = Beneficiary.objects.values()
    
    for i in count:
        if 'Active' in i.values():
            actives += 1
        elif 'Article 20.3' in i.values():
            article20 += 1
        elif 'Inactive' in i.values():
            inactives += 1
        elif 'Deceased' in i.values():
            deceased += 1 
    counts.extend([actives, article20, inactives, deceased])
    
    x = {}
    
    for key in status:
        for value in counts:
            x[key] = value
            counts.remove(value)
            break 
    
    data = pd.Series(x).reset_index(name='value').rename(columns={'index':'status'})
    data['angle'] = data['value']/data['value'].sum() * 2*pi
    data['color'] = ['green','gray','orange','red']
    color = ['green', 'gray', 'orange', 'red']

    data_csv = data.to_csv(index=True)
    
    fonts=['<i>italics</i>',
                '<pre>pre</pre>',
                '<b>bold</b>',
                '<small>small</small>',
                '<del>del</del>'
                ]
    
    hover = HoverTool(
        tooltips="""
        <div>
            <div>
                <span style="font-size: 17px; font-weight: bold; color:#966;"> <i>Status: @status</i></span>
            </div>
            <div>
                <!--<span>@fonts{safe}</span> -->
            </div>
            <div>
                <span style="font-size: 15px; font-weight: bold;">Total: @value</span>
            </div>
        </div>
        """
    )

    p = figure(plot_height=400, plot_width =750, title="Beneficiaries Count by Status", toolbar_location=None,
            tools=[hover], x_range=(-1, 1))
    
    p.outline_line_color = None
    p.title.text_font_size = '14pt'
    p.title.align = 'center'
    p.xaxis.major_label_text_font_size = '12px'
    p.xgrid.visible = False
    p.ygrid.visible = False
    p.axis.visible = False
    
    p.annular_wedge(x=0, y=1,  inner_radius=0.21, outer_radius=0.39, direction="anticlock",
            start_angle=cumsum('angle', include_zero=True), end_angle=cumsum('angle'),
            line_color="white", fill_color='color', fill_alpha = 0.6, legend_field='status', source=data)
    
    p.legend.orientation = "vertical"
    p.legend.location = "top_left"
    
    script1, div1 = components(p)
    
    # Member Status counts
    m_actives = 0
    suspend = 0
    terminate = 0
    deceased = 0
    m_counts = []
    m_status = ['Active', 'Suspended', 'Terminated', 'Deceased']
    m_count = Profile.objects.values()
    
    for i in m_count:
        if 'Active' in i.values():
            m_actives += 1
        elif 'Suspended' in i.values():
            suspend += 1
        elif 'Terminated' in i.values():
            terminate += 1
        elif 'Deceased' in i.values():
            deceased += 1 
    m_counts.extend([m_actives, suspend, terminate, deceased])
    
    # Benefiacuary QS to pandas and csv   
    qs2 = Beneficiary.objects.all()
    q2 = qs2.values('name', 'birth_date', 'beneficiary_type','beneficiary_status')
    df_ben = pd.DataFrame.from_records(q2)
    
    df_type = df_ben[['beneficiary_type']].value_counts()
    ben_csv = df_ben.to_csv(r'ben.csv')
    
    # Members Queryset to pandas and csv    
    qs1 = Profile.objects.all()
    q1 = qs1.values('shortname','birth_date','status')
    df_member = pd.DataFrame.from_records(q1)
    member_csv = df_member.to_csv(r'member.csv')
    
    
    x1 = {}
    
    for key in m_status:
        for value in m_counts:
            x1[key] = value
            m_counts.remove(value)
            break 


    data1 = pd.Series(x1).reset_index(name='value').rename(columns={'index':'m_status'})
                                                        
    data1['angle'] = data1['value']/data1['value'].sum() * 2*pi
    data1['color'] = ['green','gray','orange','red']#Category20c[len(x)
    
    fonts=['<i>italics</i>',
                '<pre>pre</pre>',
                '<b>bold</b>',
                '<small>small</small>',
                '<del>del</del>'
                ]
    
    hover = HoverTool(
        tooltips="""
        <div>
            <div>
                <span style="font-size: 17px; font-weight: bold; color:#966;"> <i> Status: @m_status</i></span>
            </div>
            <div>
                <!--<span>@fonts{safe}</span> -->
            </div>
            <div>
                <span style="font-size: 15px; font-weight: bold; ">Total: @value</span>
            </div>
        </div>
        """
    )

    p1 = figure(plot_height=400, plot_width =750, title="Members Count by Status", toolbar_location=None,
        tools=[hover], x_range=(-1, 1))
    
    p1.outline_line_color = None
    p1.title.align = 'center'
    p1.title.text_font_size = '14pt'
    p1.xaxis.major_label_text_font_size = '12px'
    p1.xgrid.visible = False
    p1.ygrid.visible = False
    p1.axis.visible = False

    p1.annular_wedge(x=0, y=1,  inner_radius=0.21, outer_radius=0.39, direction="anticlock",
            start_angle=cumsum('angle', include_zero=True), end_angle=cumsum('angle'),
            line_color="white", fill_color='color', fill_alpha = 0.6, legend_field='m_status', source=data1)
    
    p1.legend.orientation = "vertical"
    p1.legend.location = "top_left"
    
    script2, div2 = components(p1)

    # Beneficiary Dataframe
    df = pd.read_csv('ben.csv')
    df = df.drop(df[df.beneficiary_status =="Deceased"].index)
    df = df.drop(df[df.beneficiary_status =="Inactive"].index)
    
    # Member Dataframe
    df1 = pd.read_csv('member.csv')

    df1 = df1.drop(df1[df1.status =="Deceased"].index)
    df1 = df1.drop(df1[df1.status =="Terminated"].index)
    
    # Beneficiary age calculate
    def age(born):
        born = datetime.strptime(born, "%Y-%m-%d").date()
        today = date.today()
        return today.year - born.year                                         

    df['age'] = df['birth_date'].apply(age)
    df1['member_age'] = df1['birth_date'].apply(age)

    # Beneficiary Age groups definition    
    conditions = [
        (df['age'] < 18),
        (df['age'] < 36),
        (df['age'] < 50),
        (df['age'] < 60),
        (df['age'] < 70),
        (df['age'] < 80),
        (df['age'] < 90),
        (df['age'] < 100),
        (df['age'] > 99),
        ]

    values = ['Age(01 - 17)', 'Age(18 - 35)', 
            'Age(35 - 49)', 'Age(51 - 59)',
            'Age(60 - 69)', 'Age(70 - 79)',
            'Age(80 - 89)','Age(90 - 99)', 'Centenarians(100+))',
            ]

    df['age_group'] = np.select(conditions, values)

    ben_age_groups = df['age_group'].value_counts().sort_index(ascending=True)
    ben_age_groups = pd.DataFrame({'age_group':ben_age_groups.index, 'counts':ben_age_groups.values})
    # End Beneficiary age groups definition
    # Start member age groups definition
    conditions = [
        (df1['member_age'] < 50),
        (df1['member_age'] < 55),
        (df1['member_age'] < 60),
        (df1['member_age'] < 70),
        (df1['member_age'] < 80),
        (df1['member_age'] < 90),
        (df1['member_age'] <100),
        (df1['member_age'] > 99),
        ]

    values = ['Age(49 or less)', 'Age(50 - 54)',
            'Age(55 - 59)','Age(60 - 69)',
            'Age(70- 79)','Age(80 - 89)',
            'Age(90 - 99)', 'Centenarians(100+)',
            ]

    df1['m_age_group'] = np.select(conditions, values)

    
    m_age_groups = df1['m_age_group'].value_counts().sort_index(ascending=True)
    m_age_groups = pd.DataFrame({'m_age_group':m_age_groups.index, 'm_counts':m_age_groups.values})

    # Bokeh plotting Member & Beneficiary Age Groups
    ages = ben_age_groups['age_group']
    counts = ben_age_groups['counts']
    
    # Bokeh plotting for Members Age groups
    m_ages = m_age_groups['m_age_group']
    m_counts = m_age_groups['m_counts']
    
    source = ColumnDataSource(data=dict(ages=ages, counts=counts, color=Category20c[len(ben_age_groups)]))
    source1 = ColumnDataSource(data=dict(m_ages=m_ages, m_counts=m_counts, color=Category10[len(m_age_groups)]))
    
    fonts=['<i>italics</i>',
                '<pre>pre</pre>',
                '<b>bold</b>',
                '<small>small</small>',
                '<del>del</del>'
                ]
    
    hover = HoverTool(
        tooltips="""
        <div>
            <div>
                <span style="font-size: 17px; font-weight: bold; color:#966;"> <i>@ages</i></span>
            </div>
            <div>
                <!--<span>@fonts{safe}</span> -->
            </div>
            <div>
                <span style="font-size: 15px; font-weight: bold;">Total: @counts</span>
            </div>
        </div>
        """
    )

    p3 = figure(x_range=ages, y_range=(0,29), plot_height=400, plot_width =750, title="Active Beneficiaries by Age Group",
            toolbar_location=None, tools=[hover])
    
    
    hover1 = HoverTool(
        tooltips="""
        <div>
            <div>
                <span style="font-size: 17px; font-weight: bold; color:#966;">  <i>@m_ages</i></span>
            </div>
            <div>
                <!--<span>@fonts{safe}</span> -->
            </div>
            <div>
                <span style="font-size: 15px; font-weight: bold; ;"> Total: @m_counts </span>
            </div>
        </div>
        """
    ) 

    p3.vbar(x='ages', top='counts', width=0.5, color='color', fill_alpha=0.9, source=source)

    p3.outline_line_color = None
    p3.title.text_font_size = '14pt'
    p3.title.align = 'center'
    p3.xaxis.major_label_text_font_size = '12pt'
    p3.xgrid.grid_line_color = None
    p3.yaxis.minor_tick_line_color = None
    p3.xaxis.axis_label_text_color = "#850633"
    p3.yaxis.axis_label_text_color = "#850633"
    p3.yaxis.axis_label = "Age Group Count"
    p3.xaxis.axis_label = "Age Groups"
    p3.xaxis.axis_label_text_font_size= "12pt"
    p3.yaxis.axis_label_text_font_size= "12pt"

    p3.xaxis.major_label_orientation = 0.8
    
    p3.xgrid.visible = False
    p3.ygrid.visible = False
    p3.axis.visible = True
    
    script3, div3 = components(p3)
    
    # Member plot drawing    
    p4 = figure(x_range=m_ages, y_range=(0,29), plot_height=400, plot_width =750, title="Active Members by Age Group",
                toolbar_location=None, tools=[hover1])
    
    p4.vbar(x='m_ages', top='m_counts', width=0.5, color='color', fill_alpha=0.9, source=source1)

    p4.outline_line_color = None
    p4.title.text_font_size = '14pt'
    p4.title.align = 'center'
    p4.xaxis.major_label_text_font_size = '12pt'
    p4.xgrid.grid_line_color = None
    p4.yaxis.minor_tick_line_color = None
    p4.xaxis.axis_label_text_color = "#850633"
    p4.yaxis.axis_label_text_color = "#850633"
    p4.yaxis.axis_label = "Age Group Count"
    p4.xaxis.axis_label = "Age Groups"
    p4.xaxis.axis_label_text_font_size= "12pt"
    p4.yaxis.axis_label_text_font_size= "12pt"

    p4.xaxis.major_label_orientation = 0.8
    
    p4.xgrid.visible = False
    p4.ygrid.visible = False
    p4.axis.visible = True
    
    script4, div4 = components(p4)

    # show(p)
    member_tot = Profile.objects.all().count()
    ben_tot = Beneficiary.objects.all().count()
    active_members = df1.shape[0]
    active_beneficiaries = df.shape[0]

    df1.to_csv('member_csv.csv')
    df.to_csv('ben_csv.csv')
    
    return render (request, 'pmlprofile/member-dash.html', 
                    {'script1':script1, 'div1':div1,
                    'script2':script2,'div2':div2, 
                    'script3':script3, 'div3':div3, 
                    'script4':script4, 'div4':div4, 
                    'member_tot':member_tot,
                    'ben_tot':ben_tot,
                    'active_members':active_members,
                    'active_beneficiaries':active_beneficiaries}
                    )
                    
                    
class ProfileListView(LoginRequiredMixin, ListView):
    context_object_name = "profiles"
    model = Profile
    paginate_by = 9
    template_name = 'pmlprofile/member_list.html'
    
    def get_context_data(self,*args,**kwargs):
        context = super(ProfileListView, self).get_context_data(*args, **kwargs)
        context['total'] = Profile.objects.all().count()
        context['actives'] = Profile.objects.filter(status='Active').count()
        context['deceased'] = Profile.objects.filter(status='Deceased').count()
        context['suspended'] = Profile.objects.filter(status='Suspended').count()
        context['terminated'] = Profile.objects.filter(status='Terminated').count()
        return context


class ProfileDetails(LoginRequiredMixin, DetailView):
    context_object_name = 'profile_detail'
    model = Profile
    template_name = 'pmlprofile/profile_details.html'
    

@login_required
def membercert_view(request, pk):
    template_path = 'pmlprofile/member-cert.html'
    membercert = Profile.objects.get(pk=pk)
    today = date.today()
    context = {
        'membercert': membercert,
        'today': today, 
        }
    # Create a Django response object, and specify content_type as pdf
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename="report.pdf"'
    # find the template and render it.
    template = get_template(template_path)
    html = template.render(context)

# create a pdf
    pisa_status = pisa.CreatePDF(html, dest=response)

    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response

class MyProfileView(LoginRequiredMixin,DetailView):
    #login_url = '/accounts/login_view'
    context_object_name = 'my_profile'
    model = Profile
    template_name = 'pmlprofile/my_profile.html'
    
    def get_object(self):
        return self.model.objects.get(pk=self.request.user.pk)
    

class ProfileCertView(LoginRequiredMixin,DetailView):
    context_object_name = 'cert'
    model = Profile
    template_name = 'pmlprofile/cert.html'
    
    def get_object(self):
        return self.model.objects.get(pk=self.request.user.pk)
    
def pdfcert_view(request,pk):
    template_path = 'pmlprofile/pdf-cert.html'
    cert_pdf = Profile.objects.get(pk=request.user.id)
    today = date.today()
    print(today)
    context = {
        'cert_pdf': cert_pdf,
        'today': today, 
        }
    # Create a Django response object, and specify content_type as pdf
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename="member_certificate.pdf"'
    # find the template and render it.
    template = get_template(template_path)
    html = template.render(context)

    # create a pdf
    pisa_status = pisa.CreatePDF(html, dest=response)

    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response


@login_required
def profile_update(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance = request.user)
        p_form = ProfileUpdateForm(request.POST, 
                                request.FILES, 
                                instance = request.user.profile)
        
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Your profile has been succesfully updated!')
            return redirect('pmlprofile:my_profile', pk=request.user.profile.pk)
            
    else:
        u_form = UserUpdateForm(instance = request.user)
        p_form = ProfileUpdateForm(instance = request.user.profile)
        
    context = {
        'u_form':u_form,
        'p_form':p_form
    }
    return render(request, 'pmlprofile/profile_update.html',context)

    
class BeneficiaryList(LoginRequiredMixin, ListView):
    context_object_name = "beneficiaries"
    model = Beneficiary
    template_name = 'pmlprofile/beneficiary_list.hml'
    
    def get_context_data(self,*args,**kwargs):
    
        context = super(BeneficiaryList,self).get_context_data(*args, **kwargs)
        
        context['active'] = Beneficiary.objects.filter(beneficiary_status='Active').count()
        context['deceased'] = Beneficiary.objects.filter(beneficiary_status='Deceased').count()
        context['inactive'] = Beneficiary.objects.filter(beneficiary_status='Inactive').count()
        context['article20'] = Beneficiary.objects.filter(beneficiary_status='Article 20.3').count()
        context['total'] = Beneficiary.objects.all().count()
        return context


# Main Dashboard 
class CommitteeListView(LoginRequiredMixin,ListView):
    context_object_name = "committees"
    model = Committee
    print('committees')
    template_name = 'pmlprofile/committee_list.html'


class CommitteeDetail(LoginRequiredMixin, DetailView):
    context_object_name = 'committees'
    model = Committee
    template_name = 'pmlprofile/committee_details.html'
    
class CommitteeUpdateView(LoginRequiredMixin, UpdateView):
    model = Committee
    fields =['_all_']
    
    
class IncumbentCreateView(LoginRequiredMixin, CreateView):
    model = Incumbent
    success_url = reverse_lazy('pmlprofile:committees')
    fields = ['committee','member','portfolio','term_starts','term_ends']
    template_name = 'pmlprofile/committee_create.html'
    
    
class IncumbentListView(LoginRequiredMixin, ListView):
    model = Incumbent
    template_name = 'pmlprofile/'
    

class IncumbentUpdateView(LoginRequiredMixin, UpdateView):
    model = Incumbent
    success_url = reverse_lazy('pmlprofile:committees')
    fields = ['member','portfolio','term_starts','term_ends']
    

#Chartjs plots
def ben_dash(request):
    actives = 0
    article20 = 0
    inactives = 0
    deceased = 0
    status_count = []
    status_label = ['Active', 'Article 20.3', 'Inactive', 'Deceased']
    qs = Beneficiary.objects.values()
    total = Beneficiary.objects.all().count()
    
    for i in qs:
        if 'Active' in i.values():
            actives += 1
        elif 'Article 20.3' in i.values():
            article20 += 1
        elif 'Inactive' in i.values():
            inactives += 1
        elif 'Deceased' in i.values():
            deceased += 1 
    status_count.extend([actives, article20, inactives, deceased])
    print(status_label)
    print(status_count)
    context = {
        'status_label': status_label,
        'status_count': status_count,
        'total':total,
    }
    print(status_label)
    print(status_count)
    
    return render(request, 'pmlprofile/ben-dash.html', context)
    