from django.shortcuts import render
from django import forms

from .component.map import *
from .component.map_copy import copy_coords

from .service.serviceAPITravel import callAPITravel, getCoordsOfTown
from .service.serviceAPIDistance import callDistance
from .service.serviceAPITutTut import getModeleTutTutFromName
from .service.serviceAPIBorne import callAPIBorne
from .service.serviceAPICalculTemps import callTime
import requests
import math

class TutTutRecup(forms.Form):
    tuttutName = forms.CharField(label='Le modèle de votre voiture', max_length=20)
    villeFrom = forms.CharField(label='De:', max_length=20)
    villeTo = forms.CharField(label='A:', max_length=20)

def getStepTrajetCoords(extremites, nbSteps): 
    sc = []
    for i in range(0,nbSteps):
        prog = (i+1)/(nbSteps+1)
        sc.append([(1-prog)*extremites[0][0] + prog * extremites[1][0], (1-prog)*extremites[0][1] + prog * extremites[1][1]])
    return sc

# Create your views here.
def index(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')

    my_map = create_map(ip)
    folium.TileLayer('cartodbpositron').add_to(my_map)
    # folium.TileLayer('stamenwatercolor').add_to(my_map)
    # folium.TileLayer('openstreetmap').add_to(my_map)

    my_map.add_child(copy_coords(alert=False))

    if request.method == 'POST':
        tuttut = TutTutRecup(request.POST)
        if tuttut.is_valid():
            # 1 - récupérer les coordonnées des villes départ arrivée
            coords = [getCoordsOfTown(tuttut.cleaned_data['villeFrom']),getCoordsOfTown(tuttut.cleaned_data['villeTo'])]
            # 2 - API REST -> récup distance entre les points
            distanceMax = callDistance(coords)
            # 3 - GRAPHQL -> récup un des modèles correspondant au nom du véhicule
            modeleVoiture = getModeleTutTutFromName(tuttut.cleaned_data['tuttutName'])
            print(modeleVoiture)
            # 4 - autonomie = .7 * autonomie minimale de la TutTut
            autonomie = .7*modeleVoiture["range"]["chargetrip_range"]["worst"]
            # 5 - calculer coordonnées moyennes des points intermédiaires (interpolation des coordonnées maximales tmtc)
            print(distanceMax, " km")
            midCoords = getStepTrajetCoords(coords, math.floor(distanceMax/autonomie))
            print("Nb arrêt(s) : ", midCoords.__len__())
            # 6 - Chercher une borne aux environs de chacun des points moyens
            listBornes = callAPIBorne(midCoords, my_map)
            # 7 - Calculer le trajet avec étapes correspondant aux bornes
            travel = callAPITravel(coords, listBornes, my_map)
            # 8 - SOAP -> envoyer distance trajet + temps de recharge moyen + nombre d'arrêts -> temps estimé avec trajet
            tpsTrajet = callTime(distanceMax, min([c["time"] for c in modeleVoiture["connectors"]]), midCoords.__len__())
            print("Temps estimé : ", tpsTrajet, " min")
            # 9 - afficher sur la carte le trajet + temps estimé du trajet avec arrêts
            i = 0
            for p in listBornes:
                if p is None:
                    folium.Marker([midCoords[i][1],midCoords[i][0]], icon=folium.Icon(icon="hand", icon_color="white", color="red", prefix="fa")).add_to(my_map)
                else:
                    folium.Marker([p[1],p[0]], icon=folium.Icon(icon="charging-station", icon_color="white", color="lightblue", prefix="fa")).add_to(my_map)
                i+=1
            for p in coords:
                folium.Marker([p[1],p[0]]).add_to(my_map)
            
            folium.GeoJson(travel, name="Trajet").add_to(my_map)
            folium.LayerControl().add_to(my_map)
    else:
        tuttut = TutTutRecup()
        
    # Display the map
    # return HttpResponse(my_map._repr_html_())
    my_map.fit_bounds(my_map.get_bounds())
    return render(request, 'base.html', {'GigaMap': my_map._repr_html_(), 'formTutTut': tuttut})