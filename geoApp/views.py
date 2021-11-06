from django.shortcuts import render
from pmlprofile.models import Profile
from datetime import datetime, time
from .models import Location

import pandas as pd
import numpy as np

import json

def profile_geo(request):
    qs = Location.objects.all()
    
    member_list= []
    lat_list = []
    lng_list = []
    address_list = []
    for obj in qs:
        member_list.append(str(obj))
        address_list.append(obj.member.address)
        lat_list.append(float(obj.lat))
        lng_list.append(float(obj.lng))
        
    context ={
        'qs':qs,
        'member_list': member_list,
        'lat_list': lat_list,
        'lng_list': lng_list,
    }
    
    return render(request, 'geoApp/members.html',context)
    
