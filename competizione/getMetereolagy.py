import requests
import json
from datetime import datetime, timezone
import pandas
# let's send a get request to the api
zip_code="4710-057"
country_code="PT"

# Add your API key to the request URL
api_key = "ac61c74efb010f40494a5638becde9ce"



sd = datetime(2023, 1, 1, 0, 0, 0)

# Convert to UTC
utc_sd = sd.astimezone(timezone.utc)

ed = datetime(2023, 5, 5, 0, 0, 0)

# Convert to UTC
utc_ed = ed.astimezone(timezone.utc)

# Convert to UTC epoch (seconds since epoch)
sd_epoch = int(utc_sd.timestamp())
ed_epoch = int(utc_ed.timestamp())


lat = "41.5630"
lon = "-8.3933"
data = []

start = 1678820000
end = 1680650000

dataPoints = (end-start)//3600
for i in range(0,dataPoints,99):
    url = f"https://history.openweathermap.org/data/2.5/history/city?id=2742032&type=hour&start={start+i*3600}&cnt=99&appid={api_key}"
    # Send the GET request10000
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