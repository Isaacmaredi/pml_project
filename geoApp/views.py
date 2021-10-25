from django.shortcuts import render
from pmlprofile.models import Profile
from datetime import datetime, time
from .models import Location

import pandas as pd
from geopy.geocoders import ArcGIS, Nominatim

def profile_geo(request):
    qs = Profile.objects.all().values()
    print(qs)
    print('#'*10)
    

    data = pd.DataFrame(qs)
    pml_geo = data.filter(['shortname','address','town_city','district_metro'], axis=1)
    pml_geo.set_index('shortname', inplace=True)
    # print(pml_geo)
    
    # print(pml_geo)
    # name_list = list(data['shortname'])
    # pml_geo['full_address'] = pml_geo['address']  + ', ' + pml_geo['district_metro']

    # ads = list(pml_geo['full_address'])

    # pml = []
    
    
    
    # locs = ArcGIS()
    
    # lats = []
    # lons = []
    
    # for lat in ads:
    #     lat = locs.geocode(lat).latitude
    #     print(lat)
    #     lats.append(lat)
    # for lon in ads:
    #     print(lon)
    #     lon = locs.geocode(lon).longitude
    #     lons.append(lon)
    # # ends = starts - datetime.now() 
    
    # pml_data = list(zip(name_list,ads,lats,lons))
    # pml_df = pd.DataFrame(pml_data, columns=['member','address','latitude','longitude'])
    # # pml_df.to_sql(Location) 
    # pml_geo_csv = pml_df.to_csv('pmlgeo.csv') 
    # # pml_df.to_sql(Location,)
    # pml_df.set_index('Member', inplace=True)
    # print(pml_df)
    # # print('$'*30)
    # # print(pml_df)
    # # print(pml_data)
    # # print('$'*30)
    
    
    # import folium 
    
    # names = list(pml_df['Member'])
    # address = list(pml_df['Address'])
    # lat = list(pml_df['Latitude'])
    # lon = list(pml_df['Longitude'])
    
    # pml_map = folium.Map(location = [-25.696769999999958, 28.741820000000075], zoom_start = 9)
    # fg = folium.FeatureGroup(name = "PML Members Locations")
    
    # for lt, ln, addr, name in zip(lat,lon,address,name_list):
    #     print(lt,ln)
    #     fg.add_child(folium.CircleMarker(location = [lt,ln], 
    #                                     popup = (name, addr), radius = 6, color ='blue',
    #                                     fill_color = 'red', fill_opacity =0.3))
    # pml_map.add_child(fg)
    # fg.save('pmlgeo.html')
    # ends = datetime.now()

    # duration = starts - ends
    

    # pml_map = pml_map._repr_html_()
    # ctx = "Testing  csv"
    ctx = "Testing"
    context ={
        'ctx': ctx,
    }
    
    return render(request, 'geoApp/members.html',context)
    
