import urllib
import json

queryTutTut = """
    query vehicleListAll ($name: String) {
        vehicleList (search: $name) {
            naming {
                make
                model
                version
                edition
                chargetrip_version
            }
            connectors {
                time
            }
            range {
                chargetrip_range {
                    worst
                }
            }
            media {
                image {
                    url
                }
            }
        }
    }
"""

def sendRequestsWithHeaders(variables):
    
    data = {'query': queryTutTut,
            'variables': variables}
    headers = {'Accept': 'application/json',
               'Content-Type': 'application/json',
               'x-client-id': '640f10aa75ebf09179388667',
               'x-app-id': '640f10aa75ebf09179388669'
               }

    req = urllib.request.Request("https://api.chargetrip.io/graphql", json.dumps(data).encode('utf-8'), headers)

    try:
        response = urllib.request.urlopen(req)
        return response.read().decode('utf-8')
    except urllib.error.HTTPError as e:
        print((e.read()))
        print('')
        raise e

def getModeleTutTutFromName(name):
    variablesTutTut = {
        "name": "\"" + name + "\""
    }
    # Call API to find the bornes
    res = json.loads(sendRequestsWithHeaders(variablesTutTut))["data"]["vehicleList"]
    if res.__len__() == 0:
        return {"naming":{"make":"TutTutCompany", "model":"TUT TUT", "version": "E3", "edition": "CHROME", "chargetrip_version": "CHROME V2"}, "connectors": [{"time":60}], "range":{"chargetrip_range":{"worst":100}},"media":{"image":{"url":"https://www.caverne-des-jouets.com/ar-tut-tut-bolides-surprise-prudence-sos-ambulance-vtech-vehicule-1er-age-19427.jpg"}}}
    return json.loads(sendRequestsWithHeaders(variablesTutTut))["data"]["vehicleList"][0]
