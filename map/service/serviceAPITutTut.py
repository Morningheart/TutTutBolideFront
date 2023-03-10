from graphqlclient import GraphQLClient
import requests

clientTutTut = GraphQLClient(endpoint="https://api.chargetrip.io/graphql")
queryTutTut = """
query vehicleListAll ($name: String!)) {
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
#640b1ccee6ec7227c2985eec
clientTutTut.inject_token("5ed1175bad06853b3aa1e492", "x-client-id")
clientTutTut.inject_token("623996f3c35130073829b252", "x-app-id")


def getModeleTutTutFromName(name):
    variablesTutTut = {
        "search": name
    }
    
    # Call API to find the bornes
    dataTutTut = clientTutTut.execute(query=queryTutTut, variables=variablesTutTut)
    
    return dataTutTut["data"][0]

    