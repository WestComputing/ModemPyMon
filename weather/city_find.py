import json
import math
from string import hexdigits

# from weather.configuration import my_lat, my_lon

# Storage for OpenWeather API Key, latitude, longitude, nearest City ID
CONFIGURATION_FILE = 'weather/configuration.json'
# City list file downloaded from http://bulk.openweathermap.org/sample/
# Instructions: https://openweathermap.org/current#cityid
CITY_DATA_FILENAME = 'weather/city.list.json'


def find_nearest_city(latitude: float, longitude: float, log: int = 0) -> int:
    """
    Returns OpenWeather ID of nearest location
    :param longitude:
    :param latitude:
    :param log: How many entries to display (optional)
    :return: City ID of nearest weather station
    """
    ranges = get_city_data(latitude, longitude, CITY_DATA_FILENAME)
    if log:
        print(f"\nNearest weather location{'s' if log > 1 else ''}:\n")
        print("OpenWeather ID | Distance | Name")
        print("-" * 50)
        for my_range in ranges[:log]:
            print(f"{my_range['id']:>14}"
                  f" | {my_range['range']: >5.2f} mi"
                  f" | {my_range['name']}")
        print()
    return ranges[0]['id']


def get_city_data(latitude: float, longitude: float, city_data_filename: str = CITY_DATA_FILENAME) -> list:
    """
    Reads city list file downloaded from openweathermap.org
    and returns dictionary list sorted nearest-to-furthest
    :return: list
    """
    ranges = []
    cities = read_json_file(city_data_filename)
    for city in cities:
        location = {
            'id': city['id'],
            'name': city['name'],
            'lat': city['coord']['lat'],
            'lon': city['coord']['lon'],
            'range': calculate_range(latitude, longitude, city['coord']['lat'], city['coord']['lon'])
        }
        ranges.append(location)
    ranges.sort(key=lambda loc: loc['range'])
    return ranges


def read_json_file(filename: str, log: bool = False):
    try:
        with open(filename) as file:
            text = file.read()
            json_obj = json.loads(text)
    except OSError as error:
        if log:
            print("Unable to read file")
            print(error.__str__())
            exit(error.errno)
        else:
            return error
    except json.decoder.JSONDecodeError as error:
        if log:
            print("Bad configuration data")
            print(error.__str__())
            exit(2)
        else:
            return error
    return json_obj


def save_json_file(obj: dict, filename: str, log: bool = False) -> bool:
    try:
        with open(filename, 'w') as file:
            file.write(json.dumps(obj))
    except OSError as error:
        if log:
            print("Unable to read file")
            print(error.__str__())
            exit(error.errno)
        else:
            return False
    return True


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


def configure(configuration_file: str = CONFIGURATION_FILE) -> dict:
    configuration = read_configuration_file(CONFIGURATION_FILE)
    if not configuration:
        configuration = input_configuration()
    return configuration


def read_configuration_file(configuration_file: str = CONFIGURATION_FILE) -> dict:
    configuration = read_json_file(configuration_file)
    if isinstance(configuration, Exception):
        configuration = input_configuration()
    else:
        print(f"Current configuration:\n"
              f"\tAPI key: {configuration['api_key']}"
              f"\tLatitude: {configuration['latitude']}"
              f"\tLongitude: {configuration['longitude']}"
              f"\tCity ID: {configuration['city_id']}")
        keeping = get_yes_or_no("Keep current configuration")
        if not keeping:
            configuration = input_configuration()
    save_json_file(configuration, configuration_file)
    return configuration


def get_yes_or_no(prompt: str = 'Yes or no') -> bool:
    response = ''
    while not (response.startswith('y') and response.startswith('n')):
        response = input(f"{prompt} (y/n)? ").lower()
    return response.startswith('y')


def input_configuration() -> dict:
    """
    Gets API key and location from keyboard
    cf. https://home.openweathermap.org/api_keys
    :return:
    """
    api_key = input_api_key()
    latitude = input_number("your latitude", -90, 90)
    longitude = input_number("your longitude", -180, 180)
    return {
        'api_key': api_key,
        'latitude': latitude,
        'longitude': longitude,
        'city_id': find_nearest_city(latitude, longitude, 1)
    }


def input_api_key() -> str:
    api_key = ''
    while not (len(api_key) and all(digit in hexdigits for digit in api_key)):
        api_key = input("Enter OpenWeather API key: ").strip()
    return api_key


def input_number(prompt: str = "a decimal number", lower_bound: float = 0, upper_bound: float = 0) -> float:
    number = float('-inf')
    while number < lower_bound or number > upper_bound:
        string = input(f"Enter {prompt}: ")
        try:
            number = float(string)
        except ValueError:
            print(f"{prompt.title()} cannot be less than {lower_bound} or greater than {upper_bound}.")
    return number


if __name__ == '__main__':
    configure()
    # find_nearest_city(10)
