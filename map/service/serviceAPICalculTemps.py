from zeep import Client
import math

client = Client('https://tut-tut-bolide-soap.vercel.app/?wsdl')

def callTime(distanceT, tempsRecharge, nbArrets):
    res = client.service.get_traject_duration(math.ceil(distanceT), tempsRecharge, nbArrets)
    if res < 0:
        print("Le temps n'a pas pu être calculé...")
    return res