from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView,DetailView
                                
from django.views.generic.edit import UpdateView, CreateView
from .models import Profile, Beneficiary
from .forms import UserUpdateForm, ProfileUpdateForm 
from django.urls import reverse_lazy
# from .forms import UserUpdateForm, ProfileUpdateForm
# Create your views here.

# def member_list_view(request):
#     return render(request, 'pmlprofile/member_list.html')


class ProfileListView(ListView):
    context_object_name = "profiles"
    model = Profile
    template_name = 'pmlprofile/member_list.html'



class ProfileDetails(DetailView):
    context_object_name = 'profile_detail'
    model = Profile
    template_name = 'pmlprofile/profile_details.html'

class MyProfile(DetailView):
    context_object_name = 'profile_detail'
    model = Profile
    template_name = 'pmlprofile/my_profile.html'
    
    

class ProfileCreate(CreateView):
    model = Profile
    fields = ['shortname','mobile_phone', 'photo','address','town_city' ,
                'district_metro','province','alt_phone','alt_address',
            ]
    
    def form_valid(self, form):
        self.profile = form.save(commit=False)
        self.profile  = self.instance.user
        self.profile.save()
        return super().form_valid(form)    


class ProfileUpdate(UpdateView):
    model = Profile
    fields = ['shortname','middlename','birth_date', 'mobile_phone', 'photo','address','town_city' ,
                'district_metro','province','alt_phone','alt_address',
            ]   
    template_name = 'pmlprofile/profile_update.html'
    
    success_url = reverse_lazy('profile_detail')
    
    

class BeneficiaryList(ListView):
    context_object_name = "beneficiaries"
    model = Beneficiary
    template_name = 'pmlprofile/beneficiary_list.hml'
    
    
    
    
    
    
