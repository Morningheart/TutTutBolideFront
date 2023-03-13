from zeep import Client
client = Client('https://tut-tut-bolide-soap.vercel.app/?wsdl')
"""
def callTime(distanceT, tempsRecharge, nbArrets):
    


result = client.service.calculate_traject(
    45.3, 10.4, 46.3, 11.4, 100)
print(result)

# result = client.service.add(10, 20)
# print(result)
"""