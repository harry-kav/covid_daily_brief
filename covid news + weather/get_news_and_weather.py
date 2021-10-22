import json
import requests

from news_filter import get_news 
from weather_update import get_weather

with open('config.json') as config_file:
    data = json.load(config_file)
    
weather_key = data["weather_key"]
news_key = data["news_key"]
location = data["location"]

def get_data():
    '''
    extract the news and weather from the respective APIs
    '''
    try:
        news_list = get_news(news_key)
    except:
        news_list = [{'title':"No news found", "content": 'no news'}]
        
    try:
        weather_list = get_weather(location, weather_key)
    except:
        weather_list = [{"title":"No weather updates found", "content":"no weather updates"}]

    print(news_list)
    print(weather_list)
    return news_list, weather_list

