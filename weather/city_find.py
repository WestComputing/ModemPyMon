import json
import math
from weather.api_key import my_lat, my_lon

# City list file downloaded from http://bulk.openweathermap.org/sample/
CITY_DATA_FILENAME = 'weather/city.list.json'


def find_nearest_city(log=False) -> int:
    """
    Returns OpenWeather ID of nearest location
    :param log: Boolean, logs top ten locations
    :return: City ID
    """
    ranges = read_city_data(CITY_DATA_FILENAME)
    if log:
        print("\nTop ten nearest weather locations:")
        print("OpenWeather ID | Distance | Name")
        print("-" * 50)
        for my_range in ranges[:10]:
            print(f"{my_range['id']:>14}"
                  f" | {my_range['range']: >5.2f} mi"
                  f" | {my_range['name']}")
    return ranges[0]['id']


def read_city_data(city_data_filename: str) -> list:
    """
    Reads city list file downloaded from openweathermap.org
    and returns dictionary list sorted nearest-to-furthest
    :return: list
    """
    try:
        with open(city_data_filename) as file:
            text = file.read()
    except OSError:
        print("Unable to read city data file:")
        print(OSError.errno, OSError.strerror)
        print(OSError.filename)
        exit(OSError.errno)

    ranges = []
    cities = json.loads(text)
    for city in cities:
        location = {
            'id': city['id'],
            'name': city['name'],
            'lat': city['coord']['lat'],
            'lon': city['coord']['lon'],
            'range': calculate_range(my_lat, my_lon,
                                     city['coord']['lat'], city['coord']['lon'])
        }
        ranges.append(location)
    ranges.sort(key=lambda loc: loc['range'])
    return ranges


def calculate_range(lat1, lon1, lat2, lon2) -> float:
    """
    Uses Haversine Formula to calculate distance between two coordinates
    :param lat1: First location's decimal latitude
    :param lon1: First location's decimal longitude
    :param lat2: Second location's decimal latitude
    :param lon2: Second location's decimal longitude
    :return: Distance in miles
    """
    def convert_degrees_to_radians(degrees: float) -> float:
        return degrees * math.pi / 180

    lat1, lon1 = convert_degrees_to_radians(lat1), convert_degrees_to_radians(lon1)
    lat2, lon2 = convert_degrees_to_radians(lat2), convert_degrees_to_radians(lon2)
    earth_radius = 3961  # Earth's radius (miles) at 39 degrees
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = math.pow(math.sin(dlat / 2), 2) + math.cos(lat1) * math.cos(lat2) * math.pow(math.sin(dlon / 2), 2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))  # great circle distance in radians
    d = c * earth_radius
    return round(d, 2)


if __name__ == '__main__':
    find_nearest_city(True)
