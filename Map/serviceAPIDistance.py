import requests

def callDistance(coord1, coord2):
    res = requests.post("localhost:5000/distances", 
    json={"coordinates":[
        {"lon": coord1[1], "lat": coord1[0]},
        {"lon": coord2[1], "lat": coord2[0]}   
    ]})
    return res