import folium
import geocoder

def create_map(ip):
    try:
        boulder_coords = geocoder.ip(ip).latlng
        
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
    except:
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