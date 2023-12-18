import requests
import json
from datetime import datetime, timezone
import pandas
# let's send a get request to the api
zip_code="4710-057"
country_code="PT"

# Add your API key to the request URL
api_key = "ac61c74efb010f40494a5638becde9ce"
responseCoords = requests.get(f"http://api.openweathermap.org/geo/1.0/zip?zip={zip_code},{country_code}&appid={api_key}")
coords=responseCoords.json()
lat = coords['lat']
lon = coords['lon']
data = []

end = 1680645600
for start in [1678838400,1679446800,1680055200]:
    url = f"https://history.openweathermap.org/data/2.5/history/city?lat={lat}&lon={lon}&type=hour&start={start}&end={end}&appid={api_key}"
    # Send the GET request
    response = requests.get(url)

    data += response.json()['list']

def cfromk(temp):
    return temp-273.15

l2 = []
for i in data:
    i['dt_iso'] = datetime.fromtimestamp(i['dt']).strftime("%Y-%m-%d %H:%M:%S")+" +0000 UTC"
    i['city_name'] = "local"
    i['temp'] = cfromk(i['main']['temp'])
    i['feels_like'] = cfromk(i['main']['feels_like'])
    i['temp_min'] = cfromk(i['main']['temp_min'])
    i['temp_max'] = cfromk(i['main']['temp_max'])
    i['pressure'] = i['main']['pressure']
    i['sea_level'] = None
    i['grnd_level'] = None
    i['humidity'] = i['main']['humidity']
    i['wind_speed'] = i['wind']['speed']
    if "rain" in i:
        i['rain_1h'] = i['rain']['1h']
    else:
        i['rain_1h'] = None
    i['clouds_all'] = i['clouds']['all']
    i['weather_description'] = i['weather'][0]['description']
    del i['main']
    del i['weather']
    del i['clouds']
    del i['wind']
    if "rain" in i:
        del i['rain']
    l2.append(i)

df = pandas.DataFrame(l2)
df = df.round(2)
df.to_csv('metereology.csv', index=False)