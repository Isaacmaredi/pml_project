from django import forms 
from django.forms import ModelForm, Textarea
from django.contrib.auth.models import User
from .models import Profile
from crispy_forms.helper import FormHelper


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['email']
        
class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['shortname', 'middlename', 'birth_date', 'mobile_phone','alt_phone', 'photo','address','alt_address','town_city' ,'district_metro','province']
        date_field = forms.DateField(
                    widget=forms.TextInput(     
                    attrs={'type': 'date'} 
                        )
                    )        