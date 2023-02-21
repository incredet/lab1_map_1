""" LAB 1 TASK 2"""
import re
from typing import List
import argparse
from random import randint
import folium
from geopy.geocoders import Nominatim
from haversine import haversine


def open_file(locs: str) -> List[str]:
    """ this func read that huge database and returns list of values
    Args:
        str locs: path to the dataset
    Returns:
        list: list of values from the dataset
    """
    with open(locs, "r", encoding = "utf-8") as data:
        data_list = data.readlines()
        if len(data_list) - 1002 >= 1:
            counter = randint(1, len(data_list) - 1002)
        else:
            counter = 0
        data_list = data_list[counter + 16:6000 + counter]
    return data_list


def find_coords(locs: str, year: int) -> set:
    """ this func gets a year as an integer and list of movies and locations
    returns list of coordinates of locs of movies that were shot that year
    Args:
        str locs: locations where the movies was shot
        int year: the year the movies shot
    Returns:
        list: the name, the coordinates
    """
    location_set = set()
    data_list = open_file(locs)
    prev_line = ""
    for line in data_list:
        if str(year) in line:
            name = re.findall(r'\".*?\"|\'.*?\"|^[^\(]*', line)[0]
            line = re.sub("\(.*?\)|\{.*?\}|\".*?\"|\'.*?\"", "", line)
            if line != prev_line:
                prev_line = line
                try:
                    geolocator = Nominatim(user_agent="map")
                    location = geolocator.geocode(line)
                    print(location.latitude, location.longitude)
                    location_set.add((name, location.latitude, location.longitude))
                except AttributeError:
                    print(":(")
    return location_set


def calculate_distance(coordinates: set, dest_lat: float, dest_lon: float) -> List[tuple]:
    """ calculates 10 neares locations to location that is as argument to the func
    Args:
        list coordinates: list of coordinates of point on a map
        dest_lat: latitude of point to be calculated
        dest_lon: longtitude of point to be calculated
    Returns:
        list: points to be marked
    >>> calculate_distance({('"Undercover Boss"', 39.2908816, -76.610759),\
 ('"United Tastes of America"', 29.9759983, -90.0782127),\
 ('"Undercover Boss"', 40.9050988, -74.2098679), ('"Undercover Boss"', 40.826489, -74.1068091),\
 ('"Vampiro Carioca"', -22.9110137, -43.2093727), ('"Undercover Boss"', 40.7795455, -74.0237512),\
 ('"Underbelly"', 39.3703942, -74.5501546), ('"Undercover Boss"', 34.0028569, -84.1441046),\
 ('"Undercover Boss"', 39.7392364, -104.984862),\
 ('"Ven�j�n halki 30 p�iv�ss�"', 54.8053593, 83.0887559),\
 ('"Undercover Boss"', 33.7489924, -84.3902644),\
 ('"Ultimate Car Build Off"', 42.3315509, -83.0466403),\
 ('"Upstairs Downstairs"', 52.2913394, -1.536404), ('"Usta usta"', 52.215933, 19.134422)},\
 42.3315509, -83.0466403)
    [('"Ultimate Car Build Off"', 42.3315509, -83.0466403),\
 ('"Undercover Boss"', 39.2908816, -76.610759), ('"Undercover Boss"', 40.9050988, -74.2098679),\
 ('"Undercover Boss"', 40.826489, -74.1068091), ('"Undercover Boss"', 40.7795455, -74.0237512),\
 ('"Underbelly"', 39.3703942, -74.5501546), ('"Undercover Boss"', 34.0028569, -84.1441046),\
 ('"Undercover Boss"', 33.7489924, -84.3902644), ('"United Tastes of America"',\
 29.9759983, -90.0782127), ('"Undercover Boss"', 39.7392364, -104.984862)]
    """
    return sorted(list(coordinates), key = lambda coord:\
         haversine((dest_lat, dest_lon), (coord[1], coord[-1])))[:10]


def create_map(coords: list, dest_lat: float, dest_lon: float):
    """ this func creates map with mask based on 10 neares locations
        Args:
            list coords: coords to be marked
            float dest_lat: latitude of point to be circlemarked
            float dest_lon: longtitude of point to be circlemarked
        Returns:
            None
    """
    movies_map = folium.Map(location=[dest_lat, dest_lon], zoom_start=5)
    movies_locs = folium.FeatureGroup(name = "nearest locations")
    html = """<h4>Movie name: {}</h4>
    """
    for coord in coords:
        iframe = folium.IFrame(html=html.format(coord[0].strip()),
                            width=200,
                            height=50)
        movies_locs.add_child(folium.Marker(location=[coord[1], coord[-1]],\
             icon=folium.Icon(icon='cloud'), popup=folium.Popup(iframe)))
    movies_map.add_child(movies_locs)
    user_loc = folium.FeatureGroup(name = "user's location")
    html2 = """<h4>This is the location you entered. Hello there!</h4>
    """
    iframe = folium.IFrame(html=html2, width=200, height=50)
    user_loc.add_child(folium.CircleMarker(location=[dest_lat, dest_lon],\
             radius=10, popup=folium.Popup(iframe),\
                 fill_color="red", color='red', fill_opacity=0.7))
    movies_map.add_child(user_loc)
    movies_map.add_child(folium.LayerControl())
    movies_map.save("Map_Marker_irynka2.html")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("year", type = int,  help = "year the movie was made")
    parser.add_argument("lat", type = float , help = "lat")
    parser.add_argument("lon", type = float,help = "lon")
    parser.add_argument("path", type = str, help = "path to database")
    args = parser.parse_args()
    year = args.year
    lat = args.lat
    lon = args.lon
    path = args.path
    values = find_coords(path, year)
    coords = calculate_distance(values, lat, lon)
    create_map(coords, lat, lon)
