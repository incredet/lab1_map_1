""" """
import re
import folium
from geopy.geocoders import Nominatim
from typing import List
from haversine import haversine
import pandas as pd

def create_dataframe(list_of_movies: list):
    """ """
    movies = pd.DataFrame(list_of_movies, columns=['name', 'lat', 'lot'])
    return movies


def find_coords(locs: str, year) -> list:
    """ """
    location_list = []
    with open(locs, "r", encoding = "utf-8") as data:
        data_list = data.readlines()[15:]
    prev_line = ""
    for line in data_list:
        if str(year) in line:
            name = re.findall(r'\"(.*?)\"|\'(.*?)\"', line)[0][0]
            line = re.sub("\(.*?\)|\{.*?\}|\".*?\"|\'.*?\"", "", line)
            if line != prev_line:
                prev_line = line
                try:
                    geolocator = Nominatim(user_agent="map")
                    location = geolocator.geocode(line)
                    print((location.latitude, location.longitude))
                    location_list += [(name, location.latitude, location.longitude)]
                except Exception:
                    print("LocationNotFound")
    return location_list


def calculate_distance(coordinates: List[tuple], dest_lat, dest_lon) -> List[tuple]:
    """ """
    return sorted(coordinates, key = lambda coord:\
         haversine((dest_lat, dest_lon), (coord[1], coord[-1])))[:10]


def create_map(coords):
    """ """
    movies_map = folium.Map()
    movies_locs = folium.FeatureGroup(name = "nearest locations")
    for coord in coords:
        movies_locs.add_child(folium.Marker(location=[coord[1], coord[-1]],\
             icon=folium.Icon(icon='cloud')))
    movies_map.add_child(movies_locs)
    movies_map.add_child(folium.LayerControl())
    movies_map.save("Map_Marker_irynka2.html")


values = find_coords("lab1_map_1/locations_ssv.list", 2013)
print(values)
coords = calculate_distance(values, 31.7788242, 35.2257626)
create_map(coords)
