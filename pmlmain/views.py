from django.shortcuts import render, redirect
from django.http import HttpResponse
from pmlprofile.models import Committee
from django.views.generic import ListView

# Create your views here.
def index(request):
    
    objects = Committee.objects.filter(name='Executive Committee')
    
    print(objects)
    context = {
        'objects': objects,
    }
    
    return render(request,'pmlmain/index.html', context)