from django.shortcuts import render, redirect

# Create your views here.

def profile_home(request):
    return render(request, 'pmlprofile/profile_home.html')

def members(request):
    return render(request, 'pmlprofile/members.html')

def beneficiaries(request):
    return render(request, 'pmlprofile/beneficiaries.html')

def member_profile(request):
    return render(request, 'pmlprofile/member_profile.html')

