import requests
import folium
from python_graphql_client import GraphqlClient
# from .serviceAPIDistance import *

clientBorne = GraphqlClient(endpoint="https://api.placetoplug.com/go/graphql")
queryBorne = """query Query ($query: FindChargingZone!) {
                    findChargingZones(query: $query) {
                        chargingZones {
                        id
                        address {
                            street
                            city
                            country
                        }
                        status
                        coordinates
                        vehicleTypes
                        isFastCharge
                        plugTypes
                        }
                    }
                }"""

def callAPITravel(ville1,ville2, my_map):
    # Call API to find the city
    callVille1 = requests.get("https://api.openrouteservice.org/geocode/search?api_key=5b3ce3597851110001cf6248ae8b2b8cd4f943509643db9544603784&text="+ ville1 +"&boundary.country=FR")
    callVille2 = requests.get("https://api.openrouteservice.org/geocode/search?api_key=5b3ce3597851110001cf6248ae8b2b8cd4f943509643db9544603784&text="+ ville2 +"&boundary.country=FR")
    
    depart = callVille1.json()['features'][0]['geometry']['coordinates']
    dest = callVille2.json()['features'][0]['geometry']['coordinates']
    # Latitudes and longitudes
    
    # Longitudes and latitudes
    folium.Marker(location=[depart[1],depart[0]]).add_to(my_map)
    folium.Marker(location=[dest[1],dest[0]]).add_to(my_map)
    
    # body = {"coordinates":[[5.869119820356913, 45.641342957134086],[5.916631110905656, 45.67562073730605]]}
    body = {"coordinates":[depart]}

    headers = {
    'Accept': 'application/json, application/geo+json, application/gpx+xml, img/png; charset=utf-8',
    'Authorization': '5b3ce3597851110001cf6248ae8b2b8cd4f943509643db9544603784',
    'Content-Type': 'application/json; charset=utf-8'
    }
    
    # Call API to get the travel
    callTravel = requests.post("https://api.openrouteservice.org/v2/directions/driving-car/geojson", headers=headers, json=body)    
    
    temp = depart
    
    # while callDistance(temp, dest) > 100:
        
    body["coordinates"].append(temp)
                
    variablesBorne = {
        "query": {
            "limit": 1000,
            "filters": {
            "bounds": {
                "minLat": temp[1] - 1, 
                "minLon": temp[0] - 1, 
                "maxLat": temp[1] + 1, 
                "maxLon": temp[0] + 1
            }, 
            "isPublic": True
            }
        }
    }
    
    # Call API to find the bornes
    dataBorne = clientBorne.execute(query=queryBorne, variables=variablesBorne)
    
    for b in dataBorne["data"]["findChargingZones"]["chargingZones"]:
        folium.Marker(location=[b["coordinates"][1],b["coordinates"][0]]).add_to(my_map)
        
    # FinalBorne = dataBorne["data"]["findChargingZones"]["chargingZones"][0]
    # for b in dataBorne["data"]["findChargingZones"]["chargingZones"]:
    #     if callDistance(temp, b["coordinates"]) < callDistance(temp, FinalBorne["coordinates"]):
    #         FinalBorne = b

    # temp = FinalBorne["coordinates"]
    
    body["coordinates"].append(dest)
    
    # Call API to get the travel
    callTravel = requests.post("https://api.openrouteservice.org/v2/directions/driving-car/geojson", headers=headers, json=body)
    
    return callTravel.json()