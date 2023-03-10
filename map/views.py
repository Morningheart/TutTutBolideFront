from django.shortcuts import render
from django import forms

from .component.map import *
from .component.map_copy import copy_coords

from .service.serviceAPITravel import callAPITravel, getCoordsOfTown
from .service.serviceAPIDistance import callDistance
from .service.serviceAPITutTut import getModeleTutTutFromName
from .service.serviceAPIBorne import callAPIBorne
import requests

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
            # 1 - récupérer les coordonnées des villes départ arrivée
            coords = [getCoordsOfTown(tuttut.cleaned_data['villeFrom']),getCoordsOfTown(tuttut.cleaned_data['villeTo'])]
            # 2 - API REST -> récup distance entre les points
            distanceMax = callDistance(coords)
            # 3 - GRAPHQL -> récup un des modèles correspondant au nom du véhicule
            # modeleVoiture = getModeleTutTutFromName(tuttut.cleaned_data['tuttutName'])
            # 4 - autonomie = .7 * autonomie minimale de la TutTut
            autonomie = 100 # HARDCODED
            # 5 - calculer coordonnées moyennes des points intermédiaires (interpolation des coordonnées maximales tmtc)
            # ...
            # 6 - Chercher une borne aux environs de chacun des points moyens
            listBornes = callAPIBorne(tuttut.cleaned_data['villeFrom'],tuttut.cleaned_data['villeTo'], autonomie, my_map)
            # 7 - Calculer le trajet avec étapes correspondant aux bornes
            travel = callAPITravel(tuttut.cleaned_data['villeFrom'],tuttut.cleaned_data['villeTo'], my_map)
            # 8 - SOAP -> envoyer distance trajet + temps de recharge moyen (en fastcharge oui ou non) + nombre d'arrêts -> temps estimé avec trajet
            # ...
            # 9 - afficher sur la carte le trajet + temps estimé du trajet avec arrêts
            # ...
            
            folium.GeoJson(travel, name="Trajet").add_to(my_map)
            folium.LayerControl().add_to(my_map)
    else:
        tuttut = TutTutRecup()
        
    # Display the map
    # return HttpResponse(my_map._repr_html_())
    my_map.fit_bounds(my_map.get_bounds())
    return render(request, 'base.html', {'GigaMap': my_map._repr_html_(), 'formTutTut': tuttut})