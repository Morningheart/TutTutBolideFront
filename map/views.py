from django.shortcuts import render
from django import forms

from .component.map import *
from .component.map_copy import copy_coords

from .service.serviceAPITravel import callAPITravel

class TutTutRecup(forms.Form):
    tuttutName = forms.CharField(label='Le modèle de votre voiture', max_length=20)
    villeFrom = forms.CharField(label='De:', max_length=20)
    villeTo = forms.CharField(label='A:', max_length=20)

# Create your views here.
def index(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')

    my_map = create_map(ip)
    
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