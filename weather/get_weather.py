# Gets the current weather at the given spot

### IMPORTS
import requests
from datetime import datetime
from typing import Tuple

# Get API key from file
API_KEY = ''
with open('.weatherapi.key', 'r') as file:
    API_KEY = file.read().strip()
    print(API_KEY)


### CONSTANTS
WEATHERAPI = 'http://api.weatherapi.com/v1/current.json?key={}&q={},{}'

###### HELPERS #################################################
# Gets the URL to the icon from weatherapi.com and extracts only the 3 digit icon code
def get_code_from_json(forecast) -> str:
    code = forecast['condition']['icon'][-7:-4]
    return code

# Get current weather at given location
def current_weather(city: Tuple[float, float]) -> Tuple[int, int]:
    response = requests.get(WEATHERAPI.format(API_KEY, city[0], city[1]))
    data = response.json()
    weather = data['current']

    temp = int(data['current']['temp_c'])
    condition = get_code_from_json(weather)

    return (temp, condition)


if __name__ == '__main__':
    x = current_weather((39.756, -9.033))
    print(x)