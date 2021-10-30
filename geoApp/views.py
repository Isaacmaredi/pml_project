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
    
    members = []
    lat = []
    lng = []
    address = []
    for obj in qs:
        members.append(str(obj))
        address.append(obj.member.address)
        lat.append(float(obj.lat))
        lng.append(float(obj.lng))
        
    ltlng = [(lat[i],lng[i]) for i in range(len(lat))]

    loc_dict = Location.objects.values()
    print(loc_dict)

    names = [name for name in members ]
    

    
    objects = qs.values('member','lat','lng')
    geo_df = pd.DataFrame.from_records(objects)
    # print(geo_df)
    
    
    
    
    # print(lats)
    # print(lons)
    
    ctx = "Testing"
    context ={
        'qs':qs,
        'members': members,
        'lat': lat,
        'lng': lng,
    }
    
    return render(request, 'geoApp/members.html',context)
    
