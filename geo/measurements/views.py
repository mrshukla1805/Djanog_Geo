from django.shortcuts import render, get_object_or_404
from .models import Measures
from .forms import MeasurementModelForm
from geopy.geocoders import Nominatim
from geopy.distance import geodesic

from django.contrib.gis.geoip2 import GeoIP2
import folium



# Create your views here.

def cal_distance(request):

    distance = 0 
    destination = None
    obj = get_object_or_404(Measures, id=1)
    form = MeasurementModelForm(request.POST or None)
    geo = Nominatim(user_agent="geo")

    ip = '72.14.207.99'

    country, city, lat, lon = get_geo(ip)
 
    location = geo.geocode(city)
    #location

    l_lat = lat
    l_lon = lon
    A = (l_lat,l_lon)

    #initializing the map

    mp = folium.Map(width=800,height=500,location=get_centre(l_lat,l_lon))
  
    #Location Marker
    folium.Marker([l_lat,l_lon],tooltip='click here for more',popup=city['city'],
                    icon=folium.Icon(color='purple')).add_to(mp)

    
    if form.is_valid():
        instance = form.save(commit=False)
        t_destination = form.cleaned_data.get("destination")
        destination = geo.geocode(t_destination)

        #destination co-ordinates
          
        d_lat = destination.latitude
        d_lon = destination.longitude


        B = (d_lat,d_lon)

        #distance calculation
        distance = round(geodesic(A,B).km,2)

        # folium map modifications

        #initializing the map

        mp = folium.Map(width=800,height=500,location=get_centre(l_lat,l_lon,d_lat,d_lon))
  
        #Location Marker
        folium.Marker([l_lat,l_lon],tooltip='click here for more',popup=city['city'],
                    icon=folium.Icon(color='purple')).add_to(mp)

        #Destination Marker
        folium.Marker([d_lat,d_lon],tooltip='click here for more',popup=destination,
                    icon=folium.Icon(color='red', icon='cloud')).add_to(mp)


        # Now to draw the lines 

        line = folium.PolyLine(locations=[A,B],weight=4,color='blue')
        mp.add_child(line)

        instance.location = location
        instance.distance = distance
        instance.save()


    mp = mp._repr_html_()

    context = {
        'distance': distance,
        'form': form,
        'destination': destination,
        'map': mp,
    }

    return render(request, 'measurements/main.html',context)





#------------------HELPER FUNCTIONS--------------------------

def get_geo(ip):

    g= GeoIP2()
    country = g.country(ip)
    city = g.city(ip)
    lat, lon= g.lat_lon(ip)
    return country, city, lat, lon


def get_centre(latA, longA, latB=None, longB=None):
    cord = (latA, longA)

    if latB:
        cord = [(latA+latB)/2, (longA+longB)/2]

    return cord


def get_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')

    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')

    return ip