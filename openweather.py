import requests

from api_key import api_key


def fetch(city_id: int) -> dict:
    """
    Fetches open weather data by city id
    :type city_id: int
    """
    url = f'http://api.openweathermap.org/data/2.5/weather?id={str(city_id)}&appid={api_key}'
    requests_response = requests.get(url)
    response = requests_response.json()
    return response


if __name__ == '__main__':
    MCLEANSVILLE_NC = 4478715
    GREENSBORO_NC = 4469146
    GUILFORD_COUNTY_NC = 4469393
    open_weather_city_id = MCLEANSVILLE_NC
    wx_data = fetch(open_weather_city_id)
    print(wx_data)
