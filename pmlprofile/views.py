from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView,DetailView
                                
from django.views.generic.edit import UpdateView, CreateView
from .models import Profile, Beneficiary, Committee, Incumbent
from .forms import UserUpdateForm, ProfileUpdateForm 
from django.urls import reverse, reverse_lazy


class ProfileListView(LoginRequiredMixin, ListView):
    context_object_name = "profiles"
    model = Profile
    template_name = 'pmlprofile/member_list.html'



class ProfileDetails(LoginRequiredMixin, DetailView):
    context_object_name = 'profile_detail'
    model = Profile
    template_name = 'pmlprofile/profile_details.html'


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



@login_required
def my_profile(request):
    return render(request, 'pmlprofile/my_profile.html')
    
    

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
    
    
class CommitteeCreateView(CreateView):
    model = Incumbent
    success_url = reverse_lazy('pmlprofile:committees')
    fields = ['committee','member','portfolio','term_starts','term_ends']
    template_name = 'pmlprofile/committee_create.html'
    
    # def get_success_url(self):
    #     return reverse('pmlprofile:committees', kwargs={'pk': self.object.pk})
    
    
class CommitteeUpdateView(UpdateView):
    model = Incumbent
    fields = ['committee','member','portfolio','term_starts','term_ends']
    template_name = 'pmlprofile/committee_update'
