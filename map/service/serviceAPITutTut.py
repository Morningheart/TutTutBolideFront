from graphqlclient import GraphQLClient
import requests

clientTutTut = GraphQLClient(endpoint="https://api.chargetrip.io/graphql")
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
      battery {
        usable_kwh
        full_kwh
      }
      range {
        chargetrip_range {
          worst
        }
      }
      media {
        image {
          id
          type
          url
          height
          width
          thumbnail_url
          thumbnail_height
          thumbnail_width
        }
      }
    }
  }
  """
  
clientTutTut.inject_token("640f10aa75ebf09179388667", "x-client-id")
clientTutTut.inject_token("640f10aa75ebf09179388669", "x-app-id")


def getModeleTutTutFromName(name):
      
  variablesTutTut = {
    "name" : "\"" + name + "\""
  }
  
  # Call API to find the bornes
  dataTutTut = clientTutTut.execute(query=queryTutTut, variables=variablesTutTut)
  
  return dataTutTut

    