from uk_covid19 import Cov19API
import json
import requests

with open('config.json') as config_file:
    data = json.load(config_file)
    
location = data["location"]

def api_call():
	'''
	gets all covid data
	'''
	location_only = [
	    #'areaType=town',
	    'areaName='+location
	]

	cases_and_deaths = {
	    "date": "date",
	    "areaName": "areaName",
	    "areaType": "areaType",
	    "areaCode": "areaCode",
	    "newCasesByPublishDate": "newCasesByPublishDate",
	    "cumCasesByPublishDate": "cumCasesByPublishDate",
	    "newDeathsByDeathDate": "newDeathsByDeathDate",
	    "cumDeathsByDeathDate": "cumDeathsByDeathDate"
	}

	api = Cov19API(filters=location_only, structure=cases_and_deaths)

	data = api.get_json()

	covid_data = data['data']

	return covid_data

def get_covid_info(covid_data):
	'''
	filter data for deaths and cases in the last 7 days
	'''
	i = 0
	total_cases_past_7_days = 0
	total_deaths_past_7_days = 0
	for day in covid_data:
		if i == 0:
			cases_today = day['newCasesByPublishDate']
		elif i ==6:
			cases_seven_days_ago = day['newCasesByPublishDate']

		total_cases_past_7_days += day['newCasesByPublishDate']
		if i>0:
			total_deaths_past_7_days+= day['newDeathsByDeathDate']
		i+=1
		if i == 7:
			break

	return cases_today, cases_seven_days_ago, total_cases_past_7_days, total_deaths_past_7_days

def calculate_infection_rate(cases_today, cases_seven_days_ago):
	'''
	calculates the percentage change in infections throughout the past week
	'''
	absolute_change = cases_today-cases_seven_days_ago

	average_value = (cases_today+cases_seven_days_ago)/2

	infection_rate = absolute_change/average_value

	infection_rate_percentage = infection_rate * 100

	return infection_rate_percentage

def generate_covid_news():
	'''
	generate a string with all the covid news for the week
	'''

	covid_data = api_call()

	cases_today, cases_seven_days_ago, total_cases_past_7_days, total_deaths_past_7_days = get_covid_info(covid_data)

	infection_rate = round(calculate_infection_rate(cases_today, cases_seven_days_ago), 2)

	if infection_rate > 0:
		infection_statement = "The infection rate in " + location + " has increased by " + str(infection_rate) + "%"
	elif infection_rate < 0:
		infection_statement = "The infection rate in "+ location +" has decreased by " + str(-infection_rate)+ "%"
	else:
		infection_statement = "The infection rate has not changed"

	total_cases_statement = str(total_cases_past_7_days) + " new cases and "+ str(total_deaths_past_7_days) + " deaths. "

	return (infection_statement + " over the past 7 days, and there have been " + total_cases_statement.lower())

statement = generate_covid_news()
print(statement)