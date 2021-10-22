import json
import requests

def get_weather(city_name, api_key):
    '''
    this function returns the weather in a specified area
    '''
    base_url = "http://api.openweathermap.org/data/2.5/weather?"
    complete_url = base_url + "appid=" + api_key + "&q=" + city_name
    #print response object
    response = requests.get(complete_url)
    x = response.json()

    y = x["main"]
    current_temperature = y["temp"]
    current_pressure = y["pressure"]
    current_humidiy = y["humidity"]
    z = x["weather"]
    weather_description = z[0]["description"]
    # print following values
    weather_list = [{"title" : "Temperature", "content" :
    str(round(current_temperature-273.15, 2))+ "°C"}, {"title":"Atmospheric Pressure (in hPa unit)",
    "content":str(current_pressure)}, {"title":"Humidity (%)" ,"content": str(current_humidiy)}, {"title":"Description: " ,"content": str(weather_description)}]
    return weather_list



#print(get_weather("exeter","2dcd0f70506db3ebf6c40a91b9ee5fb7"))