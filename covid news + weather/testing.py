import json
from get_news_and_weather import get_data
from get_covid_info import api_call

with open('config.json') as config_file:
    data = json.load(config_file)
    
weather_key = data["weather_key"]
news_key = data["news_key"]
location = data["location"]


def test_get_data():
	assert get_data() != [{'title':"No news found", "content": 'no news'}],[{"title":"No weather updates found", "content":"no weather updates"}] 
	#get_data should return information

def test_api_call():
	assert api_call() is not None
	#the api call should return coronavirus information

test_get_data()

test_api_call()



