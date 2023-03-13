import requests
import folium

def getCoordsOfTown(town):
    ville = requests.get("https://api.openrouteservice.org/geocode/search?api_key=5b3ce3597851110001cf6248ae8b2b8cd4f943509643db9544603784&text="+ town)# +"&boundary.country=FR")
    return ville.json()['features'][0]['geometry']['coordinates']

def callAPITravel(extremites, bornes, my_map):
    # Longitudes and latitudes
    # folium.Marker(location=[extremites[0][1],extremites[0][0]]).add_to(my_map)
    # folium.Marker(location=[extremites[1][1],extremites[1][0]]).add_to(my_map)
    
    # body = {"coordinates":[[5.869119820356913, 45.641342957134086],[5.916631110905656, 45.67562073730605]]}
    body = {"coordinates":[extremites[0]] + [b for b in bornes if b is not None] + [extremites[1]]}
    print(body)

    headers = {
    'Accept': 'application/json, application/geo+json, application/gpx+xml, img/png; charset=utf-8',
    'Authorization': '5b3ce3597851110001cf6248ae8b2b8cd4f943509643db9544603784',
    'Content-Type': 'application/json; charset=utf-8'
    }    
    
    # Call API to get the travel
    callTravel = requests.post("https://api.openrouteservice.org/v2/directions/driving-car/geojson", headers=headers, json=body)
    
    return callTravel.json()