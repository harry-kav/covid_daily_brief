import json
import requests
from flask import Flask, Markup

def get_news(api_key):
	'''
	this function returns the latest headlines around the world, specifically for coronavirus and the bbc
	'''
	news = []
	notifications = []

	# Specify the query and number of returns
	parameters = {
	    #'q': 'covid-19', # query phrase
	    'pageSize': 100,  # maximum is 100
	    'country' : 'gb'
	}

	headers = {
	    'X-Api-Key': api_key,  # KEY in header to hide it from url
	}

	base_url = "http://newsapi.org/v2/top-headlines/"

	response = requests.get(base_url, params=parameters, headers=headers)
	news_dict = response.json()

	articles = news_dict["articles"]

	for article in articles:
		if "BBC" in str(article['source']) or "covid-19" in str(article['content']).strip().lower() or  "coronavirus" in str(article['content']).strip().lower():
				news.append(article)

	for article in news:
		article_link = Markup('<a href='+ str(article['url']) + '>click here</a>')
		notifications.append({"title" : str(article['title']), "content" : article_link})

	return notifications
