""" """
from geopy.geocoders import Nominatim
from geopy.geocoders import ArcGIS
import re
from typing import List
from haversine import haversine

def find_coords(locs: str, year) -> list:
    """ """
    location_list = []
    with open(locs, "r", encoding = "utf-8") as data:
        data_list = data.readlines()[15:]
    prev_line = ""
    for line in data_list:
        if str(year) in line:
            line = re.sub("\(.*?\)|\{.*?\}|\".*?\"|\'.*?\"", "", line)
            if line != prev_line:
                prev_line = line
                try:
                    geolocator = Nominatim(user_agent="map")
                    location = geolocator.geocode(line)
                    print((location.latitude, location.longitude))
                    location_list += [(location.latitude, location.longitude)]
                except Exception:
                    print("LocationNotFound")
    return location_list


def calculate_distance(coordinates: List[tuple], dest_lat, dest_lon) -> List[tuple]:
    """ """
    return sorted(coordinates, key = lambda coord:\
         haversine((dest_lat, dest_lon), (coord[0], coord[1])))[:10]



values = find_coords("lab1_map_1/locations_ssv.list", 2013)
print(calculate_distance(values, 31.7788242, 35.2257626))
