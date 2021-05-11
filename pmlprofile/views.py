from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views.generic import (View,TemplateView,ListView,
                                DetailView,CreateView,
                                UpdateView,DeleteView
                                )
from .models import Profile, Beneficiary
from .forms import UserUpdateForm, ProfileUpdateForm 
# from .forms import UserUpdateForm, ProfileUpdateForm
# Create your views here.

# def member_list_view(request):
#     return render(request, 'pmlprofile/member_list.html')


class ProfileListView(ListView):
    context_object_name = "profiles"
    model = Profile
    template_name = 'pmlprofile/member_list.html'
    paginate_by = 15


class ProfileDetails(DetailView):
    context_object_name = 'profile_detail'
    model = Profile
    template_name = 'pmlprofile/profile_details.html'
  
    
# def profile_detail_view(request):
#     return render(request, 'pmlprofile/profile_details.html')

class BeneficiaryList(ListView):
    context_object_name = "beneficiaries"
    model = Beneficiary
    template_name = 'pmlprofile/beneficiary_list.hml'
    
@login_required
def profile_update(request):
    # u_form = UserUpdateForm()
    p_form = ProfileUpdateForm()
    
    context = {
        # 'u_form': u_form,
        'p_form': p_form
    }
    
    return render(request, 'pmlprofile/profile_details.html', context)
    
    
    

    
    
    

# def beneficiary_list_view(request):
#     return render(request, 'pmlprofile/beneficiary_list.html')


def profile_create_view(request):
    return render(request, 'pmlprofile/profile_create.html')


def profile_update_view(request):
    return render(request, 'pmlprofile/profile_update.html')


def committee_create_view(request):
    return render(request, 'pmlprofile/committee_create.html')


def committee_list_view(request):
    return render(request, 'pmlprofile/committee_list.html')


def committee_update_view(request):
    return render(request, 'pmlprofile/committee_update.html')


@login_required
def profile_update(request):
    u_form = UserUpdateForm()
    p_form = UserUpdateForm()
    
    context = {
        'u_form':u_form,
        'p_form':p_form
    }
    
    return render(request, 'pmlprofile/profile_update.html', context)
    