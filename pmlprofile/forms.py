from django import forms 
from django.contrib.auth.models import User
from .models import Profile


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['email']
        
class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['shortname', 'middlename','mobile_phone','alt_phone', 'photo','address','alt_address','town_city' ,'district_metro','province']