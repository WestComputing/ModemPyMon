import json
import math
from api_key import my_lat
from api_key import my_lon

CITY_DATA_FILENAME = './city.list.json'


def deg2rad(deg: float) -> float:
    return deg * math.pi / 180  # radians = degrees * pi/180


def calculate_range(latA, lonA, latB, lonB) -> float:
    lat1 = deg2rad(latA)
    lon1 = deg2rad(lonA)
    lat2 = deg2rad(latB)
    lon2 = deg2rad(lonB)
    earth_radius = 3961  # Radius of the Earth in miles at 39 degrees, Haversine Formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = math.pow(math.sin(dlat / 2), 2) + math.cos(lat1) * math.cos(lat2) * math.pow(math.sin(dlon / 2), 2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))  # great circle distance in radians
    d = c * earth_radius
    return round(d, 2)


if __name__ == '__main__':

    with open(CITY_DATA_FILENAME) as file:
        text = file.read()
    cities = json.loads(text)

    my_ranges = []
    for city in cities:
        location = {
            'id': city['id'],
            'name': city['name'],
            'lat': city['coord']['lat'],
            'lon': city['coord']['lon'],
            'range': calculate_range(my_lat, my_lon, city['coord']['lat'], city['coord']['lon'])
        }
        my_ranges.append(location)

    my_ranges.sort(key=lambda loc: loc['range'])
    for my_range in my_ranges[:10]:
        print(f"Open Weather ID: {my_range['id']:>7} range: {my_range['range']: >5.2f} {my_range['name']}")
