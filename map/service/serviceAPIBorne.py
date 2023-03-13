import requests
import folium
import json
from graphqlclient import GraphQLClient
from .serviceAPIDistance import callDistance

clientBorne = GraphQLClient(endpoint="https://api.placetoplug.com/go/graphql")
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

def callAPIBorne(trajet, my_map):
    # Call API to find the city
    # callVille1 = requests.get("https://api.openrouteservice.org/geocode/search?api_key=5b3ce3597851110001cf6248ae8b2b8cd4f943509643db9544603784&text="+ ville1 +"&boundary.country=FR")
    # callVille2 = requests.get("https://api.openrouteservice.org/geocode/search?api_key=5b3ce3597851110001cf6248ae8b2b8cd4f943509643db9544603784&text="+ ville2 +"&boundary.country=FR")
    
    # depart = callVille1.json()['features'][0]['geometry']['coordinates']
    # dest = callVille2.json()['features'][0]['geometry']['coordinates']
    res = []
    i=1

    for t in trajet:
        print(f"{i}/{trajet.__len__()}")
        i+=1
        variablesBorne = {
            "query": {
                "limit": 1000,
                "filters": {
                "bounds": {
                    "minLat": t[1] - .5, 
                    "minLon": t[0] - .5,
                    "maxLat": t[1] + .5, 
                    "maxLon": t[0] + .5
                }, 
                "isPublic": True
                }
            }
        }
    
        # Call API to find the bornes
        dataBorne = json.loads(clientBorne.execute(query=queryBorne, variables=variablesBorne))

        if dataBorne["data"]["findChargingZones"]["chargingZones"].__len__() == 0:
            print("No charging station found")
            res.append(None)
            continue
        else:
            bornePlusProche = dataBorne["data"]["findChargingZones"]["chargingZones"][0]["coordinates"]
        
        dmin = callDistance([t, bornePlusProche])
        
        for b in dataBorne["data"]["findChargingZones"]["chargingZones"][1:]:
            tmp = callDistance([t, b["coordinates"]])
            if tmp < dmin:
                bornePlusProche = b["coordinates"]
                dmin = tmp
                        
        res.append(bornePlusProche)
        
    return res
    # FinalBorne = dataBorne["data"]["findChargingZones"]["chargingZones"][0]
    # for b in dataBorne["data"]["findChargingZones"]["chargingZones"]:
    #     if callDistance(temp, b["coordinates"]) < callDistance(temp, FinalBorne["coordinates"]):
    #         FinalBorne = b

    # temp = FinalBorne["coordinates"]