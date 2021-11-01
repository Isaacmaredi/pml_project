from django.shortcuts import render
from pmlprofile.models import Profile
from datetime import datetime, time
from .models import Location

import pandas as pd
import numpy as np

import json

# def profile_geo(request):
#     locations = [
#         [loc.lat, loc.lng, i]
#         for i, loc in enumerate(Location.objects.all())
#     ]
#     mytext = 'This the json enabled map'
#     context = {
#         'mytext': mytext,
#         'locations': json.dumps(locations)
#         }
#     print(context)
#     return render(request, 'geoApp/members.html', context)

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
        
    ltlng = [(lat_list[i],lng_list[i]) for i in range(len(lat_list))]

    loc_dict = Location.objects.values()
    print(loc_dict)

    names = [name for name in member_list]
    

    
    # objects = qs.values('member','lat','lng')
    # geo_df = pd.DataFrame.from_records(objects)
    # print(geo_df)
    
    
    
    
    # print(lats)
    # print(lons)
    
    ctx = "Testing"
    context ={
        'qs':qs,
        'member_list': member_list,
        'lat_list': lat_list,
        'lng_list': lng_list,
    }
    
    return render(request, 'geoApp/members.html',context)
    
