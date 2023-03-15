import folium
import folium.plugins

import geocoder

def create_map(ip):
    try:
        boulder_coords = geocoder.ip(ip).latlng
        
        #Create the map
        map = folium.Map(
            width='100%',
            height='80%',
            location = boulder_coords, 
            zoom_start = 13,
            control_scale=True,
            position='relative',
            tiles="cartodbpositron"
        )
        # map.add_child(folium.plugins.Fullscreen())
        return map
    
    except:
        boulder_coords = [45.64919040418908, 5.86433719433594]
        
        #Create the map
        map = folium.Map(
            width='100%',
            height='80%',
            location = boulder_coords, 
            zoom_start = 13,
            control_scale=True,
            position='relative',
            tiles="cartodbpositron"
        )
        # map.add_child(folium.plugins.Fullscreen())
        return map