from django import forms
from .models import Minutes

class MinutesForm(forms.ModelForm):
    class Meta:
        model = Minutes
        fields = ('title','doc')
    
    