#sets the directory to save the file to
import os
path = 'C:/Users/batu9/OneDrive/Documents/Code/Python/Interactive Population and Volcano Map'
os.chdir(path)

import pandas
#open and read csv data
data = pandas.read_csv("Webmap_datasources\Volcanoes.txt")
lat = list(data["LAT"])
lon = list(data["LON"])
elev = list(data["ELEV"])
name = list(data["NAME"])

#open and read json data
data_world = open("Webmap_datasources\world.json", 'r', encoding='utf-8-sig').read()
print("SUCCESS1")

#format popup
html = """<h4>Volcano information:</h4>
Name: %s </br>
Elevation: %s m </br>
Latitude: %s </br>
Longitude %s </br>
"""

#function to color marker based on elevation
def color_producer(elevation):
    if elevation < 1000:
        return 'green'
    elif 1000 <= elevation <3000:
        return 'orange'
    else:
        return "red"

#creates map with central location and zoom defined
import folium
map = folium.Map(location=[45.3288, -121.6625], zoom_start=6, tiles="Stamen Toner")

fg_overlay = folium.FeatureGroup(name="Population Overlay")
fg_markers = folium.FeatureGroup(name="Volcano Markers")

for lt, ln, el, nm in zip(lat, lon, elev, name): #iteration through lat,lon,elev,etc.. lists, extracts to variables
    
    iframe = folium.IFrame(html=html %(nm, el, lt, ln), width=200, height=150)

    #plots csv data
    fg_markers.add_child(folium.CircleMarker(
    location=[lt, ln],
    radius=6, 
    popup=folium.Popup(iframe), 
    fill_color=color_producer(el),
    color='grey',
    weight=1.5,
    fill=True,
    fill_opacity=1))

#plots json data
fg_overlay.add_child(folium.GeoJson(
data_world, 
style_function=lambda x: {'fillColor' : 'green' if x['properties']['POP2005'] < 10000000 
else 'orange' if 10000000 <= x['properties']['POP2005'] < 20000000
else 'red'}))
print("SUCCESS2")

map.add_child(fg_overlay)
map.add_child(fg_markers)

map.add_child(folium.LayerControl(
position='topright', 
collapsed=True, 
autoZIndex=True))
print("SUCCESS3")

map.save("InteractiveMap.html")

#---to test import and read data using pandas (in powershell)---
#>>>import pandas
#>>>data = pandas.read_csv("Volcanoes.txt")
#>>>data 