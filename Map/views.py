from .Map import *
from .serviceAPITravel import *

from django.shortcuts import render, get_object_or_404

# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect

from zeep import Client

import folium
import polyline
from folium.plugins import MarkerCluster
import pandas as pd
import json

from .MapComponent import copy_coords

## Soap client
# client = Client('http://192.168.167.21:8000/?wsdl')
# result1 = client.service.say_hello(
#     'Hi', 3)

# result2 = client.service.add(10, 20)

# result = str(result1) + str(result2)

{
    "bbox":[[8.8034,53.0756],[8.7834,53.0456]],
    "geojson":
        {"type":"Point","coordinates":[8.8034,53.0756]},
    "buffer":200
}

{"request":"pois","geometry":{"bbox":[[8.8034,53.0756],[8.7834,53.0456]],"geojson":{"type":"Point","coordinates":[8.8034,53.0756]},"buffer":200}}

from django import forms

# /route/v1/car/[{45.64054},{5.8712};{45.67452},{5.91606}]?steps=true&geometries=geojson

# /route/v1/car/{coordinates}?alternatives={true|false}&steps={true|false}&geometries={polyline|polyline6|geojson}&overview={full|simplified|false}&annotations={true|false}
# url = 'https://router.project-osrm.org/route/v1/driving/45.64065156855971,5.871094977724547;46.08548300818923,6.549487628404506;46.19339490626042,6.203223970603168'

# call = requests.post("https://api.openrouteservice.org/v2/directions/driving-car/geojson", headers=headers, json=body)
# call = requests.get(url)

class TutTutRecup(forms.Form):
    tuttutName = forms.CharField(label='Le modèle de votre voiture', max_length=20)
    villeFrom = forms.CharField(label='De:', max_length=20)
    villeTo = forms.CharField(label='A:', max_length=20)

def index(request):    

    my_map = create_map()
    
    my_map.add_child(copy_coords(alert=False))

    if request.method == 'POST':
        tuttut = TutTutRecup(request.POST)
        if tuttut.is_valid():
            modeleVoitureSearch = tuttut.cleaned_data['tuttutName']
            print('Modèle entré :', modeleVoitureSearch)
            travel = callAPITravel(tuttut.cleaned_data['villeFrom'],tuttut.cleaned_data['villeTo'], my_map)
            folium.GeoJson(travel, name="Trajet").add_to(my_map)
            folium.LayerControl().add_to(my_map)
    else:
        tuttut = TutTutRecup()
        
    # Display the map
    # return HttpResponse(my_map._repr_html_())
    my_map.fit_bounds(my_map.get_bounds())
    return render(request, 'base.html', {'GigaMap': my_map._repr_html_(), 'formTutTut': tuttut})