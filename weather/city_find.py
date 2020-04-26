import json
import math
from weather.configuration import my_lat, my_lon

# City list file downloaded from http://bulk.openweathermap.org/sample/
# Instructions: https://openweathermap.org/current#cityid
CITY_DATA_FILENAME = 'weather/city.list.json'


def find_nearest_city(log: int = 0) -> int:
    """
    Returns OpenWeather ID of nearest location
    :param log: How many entries to display (optional)
    :return: City ID of nearest weather station
    """
    ranges = read_city_data(CITY_DATA_FILENAME)
    if log:
        print(f"\nTop {log} closest weather locations:\n")
        print("OpenWeather ID | Distance | Name")
        print("-" * 50)
        for my_range in ranges[:log]:
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
    except OSError as error:
        print("Unable to read city data file")
        print(error.__str__())
        exit(error.errno)

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
    earth_radius = 3961  # Earth's radius (miles) at 39 degrees
    lat1, lon1, lat2, lon2 = map(lambda deg: deg * math.pi / 180, [lat1, lon1, lat2, lon2])
    dlat, dlon = lat2 - lat1, lon2 - lon1
    a = math.pow(math.sin(dlat / 2), 2) + math.cos(lat1) * math.cos(lat2) * math.pow(math.sin(dlon / 2), 2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))  # great circle distance in radians
    d = c * earth_radius
    return round(d, 2)


if __name__ == '__main__':
    find_nearest_city(10)
