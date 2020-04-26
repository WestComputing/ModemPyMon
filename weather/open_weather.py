import requests
from weather.configuration import api_key
from weather.city_find import find_nearest_city


def fetch(city_id: int) -> dict:
    """
    Fetches open weather map data by city id
    :type city_id: int
    """
    url = f'http://api.openweathermap.org/data/2.5/weather?id={str(city_id)}&appid={api_key}&units=imperial'
    requests_response = requests.get(url)
    response = requests_response.json()
    return response


if __name__ == '__main__':
    # MCLEANSVILLE_NC = 4478715
    open_weather_city_id = find_nearest_city()
    wx_data = fetch(open_weather_city_id)
    print(wx_data)
