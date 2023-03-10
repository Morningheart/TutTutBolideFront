from python_graphql_client import GraphqlClient
import requests

clientTutTut = GraphqlClient(endpoint="https://api.chargetrip.io/graphql")
queryTutTut = """query vehicleListFilter($query: vehicleList!) {
                    vehicleList(query: $query) {
                        id
                        naming {
                            model
                            version
                            edition
                        }
                        range {
                            worst {
                                combined {
                                    unit=meter
                                }
                            }
                            chargetrip_range {
                                worst {

                                }
                            }
                        }
                    }
                }"""
clientTutTut.inject_token("5ed1175bad06853b3aa1e492", "x-client-id")
clientTutTut.inject_token("623996f3c35130073829b252","x-app-id")


def getModeleTutTutFromName(name):
    return name
    variablesTutTut = {
        "query": {
            "search": name,
            "size": 1
        }
    }
    
    # Call API to find the bornes
    dataTutTut = clientTutTut.execute(query=queryTutTut, variables=variablesTutTut)

    