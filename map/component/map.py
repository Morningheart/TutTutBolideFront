import folium
# from ipregistry import IpregistryClient

def create_map():
    # client = IpregistryClient("tryout")  
    # ipInfo = client.lookup() 
    # print(ipInfo)

    #Define coordinates of where we want to center our map
    boulder_coords = [45.64919040418908, 5.86433719433594]

    #Create the map
    return folium.Map(
        width='100%',
        height='100%',
        location = boulder_coords, 
        zoom_start = 13,
        control_scale=True,
        position='absolute',
        tiles="cartodbpositron"
        )   