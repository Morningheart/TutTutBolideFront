import requests
import folium
from graphqlclient import GraphQLClient

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

def callAPIBorne(ville1,ville2, autonomie, my_map):
    # Call API to find the city
    callVille1 = requests.get("https://api.openrouteservice.org/geocode/search?api_key=5b3ce3597851110001cf6248ae8b2b8cd4f943509643db9544603784&text="+ ville1 +"&boundary.country=FR")
    callVille2 = requests.get("https://api.openrouteservice.org/geocode/search?api_key=5b3ce3597851110001cf6248ae8b2b8cd4f943509643db9544603784&text="+ ville2 +"&boundary.country=FR")
    
    depart = callVille1.json()['features'][0]['geometry']['coordinates']
    dest = callVille2.json()['features'][0]['geometry']['coordinates']
    
    variablesBorne = {
        "query": {
            "limit": 1000,
            "filters": {
            "bounds": {
                "minLat": depart[1] - 1, 
                "minLon": depart[0] - 1, 
                "maxLat": dest[1] + 1, 
                "maxLon": dest[0] + 1
            }, 
            "isPublic": True
            }
        }
    }
    
    # Call API to find the bornes
    dataBorne = clientBorne.execute(query=queryBorne, variables=variablesBorne)
    
    for b in dataBorne["findChargingZones"]["chargingZones"]:
        icone = folium.Icon(icon="charging-station", icon_color="white", color="lightblue", prefix="fa")
        folium.Marker(location=[b["coordinates"][1],b["coordinates"][0]], icon=icone).add_to(my_map)
        
    # FinalBorne = dataBorne["data"]["findChargingZones"]["chargingZones"][0]
    # for b in dataBorne["data"]["findChargingZones"]["chargingZones"]:
    #     if callDistance(temp, b["coordinates"]) < callDistance(temp, FinalBorne["coordinates"]):
    #         FinalBorne = b

    # temp = FinalBorne["coordinates"]