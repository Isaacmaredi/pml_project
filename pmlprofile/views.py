from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView,DetailView
                                
from django.views.generic.edit import UpdateView, CreateView
from .models import Profile, Beneficiary, Committee, Incumbent
from .forms import UserUpdateForm, ProfileUpdateForm 
from django.urls import reverse, reverse_lazy

import os
from django.conf import settings
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.contrib.staticfiles import finders


class ProfileListView(LoginRequiredMixin, ListView):
    context_object_name = "profiles"
    model = Profile
    template_name = 'pmlprofile/member_list.html'
    
    def get_context_data(self,*args,**kwargs):
        context = super(ProfileListView, self).get_context_data(*args, **kwargs)
        context['actives'] = Profile.objects.filter(status='Active').count()
        context['deceased'] = Profile.objects.filter(status='Deceased').count()
        return context


class ProfileDetails(LoginRequiredMixin, DetailView):
    context_object_name = 'profile_detail'
    model = Profile
    template_name = 'pmlprofile/profile_details.html'

class MyProfileView(LoginRequiredMixin,DetailView):
    context_object_name = 'my_profile'
    model = Profile
    template_name = 'pmlprofile/my_profile.html'

class ProfileCertView(LoginRequiredMixin,DetailView):
    context_object_name = 'certificate'
    model = Profile
    template_name = 'pmlprofile/cert.html'
    
def pdfcert_view(request):
    template_path = 'pmlprofile/pdf-cert.html'
    my_cert = Profile.objects.all()
    context = {
        'my_cert': my_cert
        }
    # Create a Django response object, and specify content_type as pdf
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="mycert.pdf"'
    # find the template and render it.
    template = get_template(template_path)
    html = template.render(context)

    # create a pdf
    pisa_status = pisa.CreatePDF(
        html, dest=response)
    # if error then show some funy view
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
            return redirect('pmlprofile:my_profile')
            
    else:
        u_form = UserUpdateForm(instance = request.user)
        p_form = ProfileUpdateForm(instance = request.user.profile)
        
    context = {
        'u_form':u_form,
        'p_form':p_form
    }
    return render(request, 'pmlprofile/profile_update.html',context)
    

class BeneficiaryList(ListView):
    context_object_name = "beneficiaries"
    model = Beneficiary
    template_name = 'pmlprofile/beneficiary_list.hml'
    
    
class CommitteeListView(ListView):
    context_object_name = "committees"
    model = Committee
    print('committees')
    template_name = 'pmlprofile/committee_list.html'

class CommitteeDetail(LoginRequiredMixin, DetailView):
    context_object_name = 'committees'
    model = Committee
    template_name = 'pmlprofile/committee_details.html'
    
class CommitteeUpdateView(UpdateView):
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
    
    # def get_success_url(self):
    #     return reverse('pmlprofile:committees', kwargs={'pk': self.object.pk})
    
    
class IncumbentUpdateView(LoginRequiredMixin, UpdateView):
    model = Incumbent
    success_url = reverse_lazy('pmlprofile:committees')
    fields = ['member','portfolio','term_starts','term_ends']
    
    
