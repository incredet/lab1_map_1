""" """
import re
from typing import List
import folium
from geopy.geocoders import Nominatim
from haversine import haversine
import pandas as pd
from random import randint
import argparse

def create_dataframe(list_of_movies: list):
    """ """
    movies = pd.DataFrame(list_of_movies, columns=['name', 'lat', 'lot'])
    return movies


def open_file(locs: str) -> list:
    """ """
    with open(locs, "r", encoding = "utf-8") as data:
        data_list = data.readlines()
        if len(data_list) - 6000 >= 1:
            counter = randint(1, len(data_list) - 6002)
        else:
            counter = 0
        data_list = data_list[counter + 16:6000 + counter]
    return data_list


def find_coords(locs: str, year) -> list:
    """ """
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


def calculate_distance(coordinates: List[tuple], dest_lat, dest_lon) -> List[tuple]:
    """ """
    return sorted(list(coordinates), key = lambda coord:\
         haversine((dest_lat, dest_lon), (coord[1], coord[-1])))[:10]


def create_map(coords, dest_lat, dest_lon):
    """ """
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
             radius=10, popup=folium.Popup(iframe), fill_color="red", color='red', fill_opacity=0.7))
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
    # values = find_coords(path, year)
    values = {('"Undercover Boss"', 30.2711286, -97.7436995), ('"Underbelly"', 39.9005585, -74.93389105589023), ('"Unseen"', 34.0536909, -118.242766), ('"United Tastes of America"', 42.3554334, -71.060511), ('"Untitled Fiction Project"', 34.0536909, -118.242766), ('"Up All Night"', 39.7027677, -75.1119434), ('"Undercover Boss"', 40.7127281, -74.0060152), ('"Undercover Boss"', 39.0273676, -95.7627535), ('"United Tastes of America"', 33.7489924, -84.3902644), ('"Undercover Boss"', 34.0007493, -81.0343313), ('"Ultimate Car Build Off"', 34.0536909, -118.242766), ('"Tuuri"', 62.6016174, 23.7325656), ('"Undercover Boss"', 34.8629426, -111.8137097), ('"Undercover Boss"', 33.6633386, -117.903317), ('"Undercover Boss"', 32.7884363, -79.9399309), ('"Tucson Morning Blend"', 32.2228765, -110.9748477), ('"United Tastes of America"', 34.0536909, -118.242766), ('"VIP Television"', 26.318342, -80.0996306), ('"Universal Dead"', 32.8528287, -116.6158525), ('"Vancouver 2010: XXI Olympic Winter Games"', 49.2608724, -123.113952), ('"Ven�j�n halki 30 p�iv�ss�"', 56.3264816, 44.0051395), ('"Undercover Boss"', 40.9312099, -73.8987469), ('"United Tastes of America"', 40.7127281, -74.0060152), ('"Vasl"', 27.7567667, -81.4639835), ('"Universal Dead"', 32.7174202, -117.1627728), ('"T�k�s-M�kos"', 47.4979937, 19.0403594), ('"Unusual Suspects"', 34.3916641, -118.542586), ('"Unusual Suspects"', 34.1684364, -118.6058382), ('"Undercover Boss"', 37.050096, -121.9905908), ('"Undercover Boss"', 26.640628, -81.8723084), ('"Undercover Boss"', 33.8322043, -118.2517547), ('"Ven�j�n halki 30 p�iv�ss�"', 43.1150678, 131.8855768), ('"Unusual Suspects"', 35.0525759, -78.878292), ('"Undercover Boss"', 37.7790262, -122.419906), ('"Upstairs Downstairs"', 51.5615216, -3.028338912531903), ('"Undercover Boss"', 27.9477595, -82.458444), ('"T�s Aqui, T�s Apanhado"', 38.7077507, -9.1365919), ('"VIP Television"', 26.1723065, -80.1319893), ('"Undercover Boss"', 33.7738353, -116.35205662407918), ('"Undercover Boss"', 26.0031465, -80.223937), ('"Upstairs Downstairs"', 52.2947017, -1.5394781), ('"Unusual Suspects"', 34.0536909, -118.242766), ('"Vamped Out"', 34.0536909, -118.242766), ('"Undercover Boss"', 38.6280278, -90.1910154), ('"Undercover Boss"', 45.7874957, -108.49607), ('"Vancouver 2010: XXI Olympic Winter Games"', 50.1171903, -122.9543022), ('"Ven�j�n halki 30 p�iv�ss�"', 56.839104, 60.60825), ('"United Tastes of America"', 30.2711286, -97.7436995), ('"Undercover Boss"', 33.4484367, -112.074141), ('"Two-Way Street"', 40.7127281, -74.0060152), ('"Undercover Boss"', 36.1622767, -86.7742984), ('"VIP Television"', 26.4614625, -80.0728201), ('"Two Minute Meals with Champ"', 41.8755616, -87.6244212), ('"Undercover Boss"', 39.5261206, -119.8126581), ('"Ven�j�n halki 30 p�iv�ss�"', 60.1674881, 24.9427473), ('"Undercover Boss"', 29.9759983, -90.0782127), ('"Ull per ull"', 41.3828939, 2.1774322), ('"Undercover Boss"', 40.6916081, -75.2099866), ('"Ultimate European Road Trip"', 38.9953683, 21.9877132), ('"Undercover Boss"', 39.9622601, -83.0007065), ('"Undercover Boss"', 30.6867339, -88.0848929), ('"Up Up Down Down: The Series"', 34.1649502, -118.3747521), ('"United Tastes of America"', 41.8755616, -87.6244212), ('"Twentysixmiles"', 33.7690164, -118.191604), ('"VIP Television"', 26.1223084, -80.1433786), ('"United Tastes of America"', 35.6876096, -105.938456), ('"Undercover Boss"', 38.8950368, -77.0365427), ('"Undercover Boss"', 41.2587459, -95.9383758), ('"Undercover Boss"', 34.4458248, -119.0779359), ('"Uusi p�iv�"', 61.4980214, 23.7603118), ('"Turn Back Time: The High Street"', 51.1910949, -2.5467475), ('"Undercover Boss"', 25.7741728, -80.19362), ('"Uau!"', 40.4167047, -3.7035825), ('"Undercover Boss"', 32.9529927, -96.9085624), ('"Undercover Boss"', 29.7589382, -95.3676974), ('"Undercover Boss"', 25.9406488, -80.2456045), ('"Undercover Boss"', 35.2503394, -112.1869481), ('"Undercover Boss"', 34.1508718, -118.4489865), ('"Ven�j�n halki 30 p�iv�ss�"', 55.7504461, 37.6174943), ('"Under SF"', 37.7790262, -122.419906), ('"Undercover Boss"', 41.94813535, -87.65635154722081), ('"Undercover Boss"', 40.2876108, -74.1723652), ('"Undercover Boss"', 38.9013729, -77.2651762), ('"Undercover Boss"', 37.9577016, -121.2907796), ('"Undercover Boss"', 35.0525759, -78.878292), ('"Undercover Boss"', 40.9397796, -74.1312504), ('"Ven�j�n halki 30 p�iv�ss�"', 51.6312684, 136.121524), ('"Undercover Boss"', 22.8938884, -109.9200604), ('"Ultimate European Road Trip"', 48.8588897, 2.3200410217200766), ('"VIP Television"', 25.7929198, -80.1353006), ('"United Tastes of America"', 37.7790262, -122.419906), ('"Ven�j�n halki 30 p�iv�ss�"', 51.8357841, 107.5839105), ('"Ull per ull"', 41.5421013, 2.1138977), ('"Ultimate Car Build Off"', 33.7489924, -84.3902644), ('"Undercover Boss"', 35.9603948, -83.9210261), ('"Unusual Suspects"', 34.1591324, -118.5016166), ('"Ultimate European Road Trip"', 51.5073359, -0.12765), ('"Vampire Zombie Werewolf"', 34.0536909, -118.242766), ('"Underbelly"', 39.731681, -75.1300457), ('"Undercover Boss"', 34.0211224, -118.396466), ('"Vancity Calling"', 49.2608724, -123.113952), ('"Unnatural History"', 43.6534817, -79.3839347), ('"Upstairs Downstairs"', 52.2946327, -1.5392146), ('"Undercover Boss"', 39.2908816, -76.610759), ('"Ven�j�n halki 30 p�iv�ss�"', 56.6370122, 104.719221), ('"United Tastes of America"', 29.9759983, -90.0782127), ('"Undercover Boss"', 40.9050988, -74.2098679), ('"Undercover Boss"', 40.826489, -74.1068091), ('"Vampiro Carioca"', -22.9110137, -43.2093727), ('"Undercover Boss"', 40.7795455, -74.0237512), ('"Undercover Boss"', 43.9441328, -90.8129118), ('"Underbelly"', 39.3703942, -74.5501546), ('"Undercover Boss"', 34.0028569, -84.1441046), ('"Under Ether"', 52.865196, -7.9794599), ('"Undercover Boss"', 39.7392364, -104.984862), ('"Ven�j�n halki 30 p�iv�ss�"', 54.8053593, 83.0887559), ('"Undercover Boss"', 33.7489924, -84.3902644), ('"Up Up Down Down: The Series"', 34.0980031, -118.329523), ('"Urbanus Vertelt"', 50.9287524, 4.4228712), ('"Ultimate Car Build Off"', 42.3315509, -83.0466403), ('"Upstairs Downstairs"', 52.2913394, -1.536404), ('"Usta usta"', 52.215933, 19.134422), ('"Undercover Boss"', 25.4718946, -80.4759905), ('"Undercover Boss"', 33.4151005, -111.8314552), ('"Undercover Boss"', 34.0536909, -118.242766)}
    coords = calculate_distance(values, lat, lon)
    create_map(coords, lat, lon)
# print(values)
values = {('"Undercover Boss"', 30.2711286, -97.7436995), ('"Underbelly"', 39.9005585, -74.93389105589023), ('"Unseen"', 34.0536909, -118.242766), ('"United Tastes of America"', 42.3554334, -71.060511), ('"Untitled Fiction Project"', 34.0536909, -118.242766), ('"Up All Night"', 39.7027677, -75.1119434), ('"Undercover Boss"', 40.7127281, -74.0060152), ('"Undercover Boss"', 39.0273676, -95.7627535), ('"United Tastes of America"', 33.7489924, -84.3902644), ('"Undercover Boss"', 34.0007493, -81.0343313), ('"Ultimate Car Build Off"', 34.0536909, -118.242766), ('"Tuuri"', 62.6016174, 23.7325656), ('"Undercover Boss"', 34.8629426, -111.8137097), ('"Undercover Boss"', 33.6633386, -117.903317), ('"Undercover Boss"', 32.7884363, -79.9399309), ('"Tucson Morning Blend"', 32.2228765, -110.9748477), ('"United Tastes of America"', 34.0536909, -118.242766), ('"VIP Television"', 26.318342, -80.0996306), ('"Universal Dead"', 32.8528287, -116.6158525), ('"Vancouver 2010: XXI Olympic Winter Games"', 49.2608724, -123.113952), ('"Ven�j�n halki 30 p�iv�ss�"', 56.3264816, 44.0051395), ('"Undercover Boss"', 40.9312099, -73.8987469), ('"United Tastes of America"', 40.7127281, -74.0060152), ('"Vasl"', 27.7567667, -81.4639835), ('"Universal Dead"', 32.7174202, -117.1627728), ('"T�k�s-M�kos"', 47.4979937, 19.0403594), ('"Unusual Suspects"', 34.3916641, -118.542586), ('"Unusual Suspects"', 34.1684364, -118.6058382), ('"Undercover Boss"', 37.050096, -121.9905908), ('"Undercover Boss"', 26.640628, -81.8723084), ('"Undercover Boss"', 33.8322043, -118.2517547), ('"Ven�j�n halki 30 p�iv�ss�"', 43.1150678, 131.8855768), ('"Unusual Suspects"', 35.0525759, -78.878292), ('"Undercover Boss"', 37.7790262, -122.419906), ('"Upstairs Downstairs"', 51.5615216, -3.028338912531903), ('"Undercover Boss"', 27.9477595, -82.458444), ('"T�s Aqui, T�s Apanhado"', 38.7077507, -9.1365919), ('"VIP Television"', 26.1723065, -80.1319893), ('"Undercover Boss"', 33.7738353, -116.35205662407918), ('"Undercover Boss"', 26.0031465, -80.223937), ('"Upstairs Downstairs"', 52.2947017, -1.5394781), ('"Unusual Suspects"', 34.0536909, -118.242766), ('"Vamped Out"', 34.0536909, -118.242766), ('"Undercover Boss"', 38.6280278, -90.1910154), ('"Undercover Boss"', 45.7874957, -108.49607), ('"Vancouver 2010: XXI Olympic Winter Games"', 50.1171903, -122.9543022), ('"Ven�j�n halki 30 p�iv�ss�"', 56.839104, 60.60825), ('"United Tastes of America"', 30.2711286, -97.7436995), ('"Undercover Boss"', 33.4484367, -112.074141), ('"Two-Way Street"', 40.7127281, -74.0060152), ('"Undercover Boss"', 36.1622767, -86.7742984), ('"VIP Television"', 26.4614625, -80.0728201), ('"Two Minute Meals with Champ"', 41.8755616, -87.6244212), ('"Undercover Boss"', 39.5261206, -119.8126581), ('"Ven�j�n halki 30 p�iv�ss�"', 60.1674881, 24.9427473), ('"Undercover Boss"', 29.9759983, -90.0782127), ('"Ull per ull"', 41.3828939, 2.1774322), ('"Undercover Boss"', 40.6916081, -75.2099866), ('"Ultimate European Road Trip"', 38.9953683, 21.9877132), ('"Undercover Boss"', 39.9622601, -83.0007065), ('"Undercover Boss"', 30.6867339, -88.0848929), ('"Up Up Down Down: The Series"', 34.1649502, -118.3747521), ('"United Tastes of America"', 41.8755616, -87.6244212), ('"Twentysixmiles"', 33.7690164, -118.191604), ('"VIP Television"', 26.1223084, -80.1433786), ('"United Tastes of America"', 35.6876096, -105.938456), ('"Undercover Boss"', 38.8950368, -77.0365427), ('"Undercover Boss"', 41.2587459, -95.9383758), ('"Undercover Boss"', 34.4458248, -119.0779359), ('"Uusi p�iv�"', 61.4980214, 23.7603118), ('"Turn Back Time: The High Street"', 51.1910949, -2.5467475), ('"Undercover Boss"', 25.7741728, -80.19362), ('"Uau!"', 40.4167047, -3.7035825), ('"Undercover Boss"', 32.9529927, -96.9085624), ('"Undercover Boss"', 29.7589382, -95.3676974), ('"Undercover Boss"', 25.9406488, -80.2456045), ('"Undercover Boss"', 35.2503394, -112.1869481), ('"Undercover Boss"', 34.1508718, -118.4489865), ('"Ven�j�n halki 30 p�iv�ss�"', 55.7504461, 37.6174943), ('"Under SF"', 37.7790262, -122.419906), ('"Undercover Boss"', 41.94813535, -87.65635154722081), ('"Undercover Boss"', 40.2876108, -74.1723652), ('"Undercover Boss"', 38.9013729, -77.2651762), ('"Undercover Boss"', 37.9577016, -121.2907796), ('"Undercover Boss"', 35.0525759, -78.878292), ('"Undercover Boss"', 40.9397796, -74.1312504), ('"Ven�j�n halki 30 p�iv�ss�"', 51.6312684, 136.121524), ('"Undercover Boss"', 22.8938884, -109.9200604), ('"Ultimate European Road Trip"', 48.8588897, 2.3200410217200766), ('"VIP Television"', 25.7929198, -80.1353006), ('"United Tastes of America"', 37.7790262, -122.419906), ('"Ven�j�n halki 30 p�iv�ss�"', 51.8357841, 107.5839105), ('"Ull per ull"', 41.5421013, 2.1138977), ('"Ultimate Car Build Off"', 33.7489924, -84.3902644), ('"Undercover Boss"', 35.9603948, -83.9210261), ('"Unusual Suspects"', 34.1591324, -118.5016166), ('"Ultimate European Road Trip"', 51.5073359, -0.12765), ('"Vampire Zombie Werewolf"', 34.0536909, -118.242766), ('"Underbelly"', 39.731681, -75.1300457), ('"Undercover Boss"', 34.0211224, -118.396466), ('"Vancity Calling"', 49.2608724, -123.113952), ('"Unnatural History"', 43.6534817, -79.3839347), ('"Upstairs Downstairs"', 52.2946327, -1.5392146), ('"Undercover Boss"', 39.2908816, -76.610759), ('"Ven�j�n halki 30 p�iv�ss�"', 56.6370122, 104.719221), ('"United Tastes of America"', 29.9759983, -90.0782127), ('"Undercover Boss"', 40.9050988, -74.2098679), ('"Undercover Boss"', 40.826489, -74.1068091), ('"Vampiro Carioca"', -22.9110137, -43.2093727), ('"Undercover Boss"', 40.7795455, -74.0237512), ('"Undercover Boss"', 43.9441328, -90.8129118), ('"Underbelly"', 39.3703942, -74.5501546), ('"Undercover Boss"', 34.0028569, -84.1441046), ('"Under Ether"', 52.865196, -7.9794599), ('"Undercover Boss"', 39.7392364, -104.984862), ('"Ven�j�n halki 30 p�iv�ss�"', 54.8053593, 83.0887559), ('"Undercover Boss"', 33.7489924, -84.3902644), ('"Up Up Down Down: The Series"', 34.0980031, -118.329523), ('"Urbanus Vertelt"', 50.9287524, 4.4228712), ('"Ultimate Car Build Off"', 42.3315509, -83.0466403), ('"Upstairs Downstairs"', 52.2913394, -1.536404), ('"Usta usta"', 52.215933, 19.134422), ('"Undercover Boss"', 25.4718946, -80.4759905), ('"Undercover Boss"', 33.4151005, -111.8314552), ('"Undercover Boss"', 34.0536909, -118.242766)}

