import requests

def callDistance(coords):
    res = requests.post("https://tut-tut-bolide-rest.vercel.app/distance", 
    json={"coordinates":[
        {"lon": coords[0][1], "lat": coords[0][0]},
        {"lon": coords[1][1], "lat": coords[1][0]}   
    ]})
    return res