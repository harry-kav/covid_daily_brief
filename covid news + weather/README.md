README:

covid news + weather app:

description:
	This application provides real-time news and weather updates, as well as
	an alarm that is scheduled by the user, which announces the current coronavirus
	news. It will also announce news and/or weather if the user requests it.
	The alarm will repeat itself, so that the user does not
	miss it.

	API keys and calls can be tested in testing.py

installation prerequisites:
	To run this app, you will need to pip install:
		pyttsx3
		uk-covid19
		flask
		sched

other prerequisites:
	In the config.json file, you will need to add:
		an API key for newsapi.org
		an API key for openweathermap.org
		a location

	You can also change the intervals in the config.json file

	Other modules used are:
		datetime, time, requests

Module descriptions:

	news_filter:

		get_news(api_key)
			This function gets the top headlines from around the world, and filters for
			coronavirus news

	weather_update:
		get_weather(city_name, api_key)
			This gets the weather in your specified area

	get_news_and_weather:
		get_data()
			This collects the news and weather to return to main.py

	get_covid_info.py:
		api_call()
			sets up the api call and returns all covid data

		get_covid_info(covid_data)
			collects the covid information that will be used in announcements

	time_manager.py:
		hhmm_to_seconds(hhmm: str)
			converts a time given in hhmm format to seconds
		
		hours_to_minutes(hours: str)
			converts hours to minutes

		minutes_to_seconds(minutes: str)
			converts minutes to seconds

		current_time_hhmm()
			returns the current time

	main.py:
		clear_removed_notifications()
			after a certain amount of time(specified in config), clear removed notifications
		
		cancel_and_close(cancelled_alarm, closed_notification)
			cancel alarms and close notifications upon user request
	
		check_alarms()
			on an interval, remove any alarms that have already passed

		check_alarm_file()
			this function checks the alarm file when the server starts, loading future alarms and deleting past alarms

		index()
			the main page- setting the alarm is handled here

		get_alarm_information(info_string)
			converts the information in the alarm to the latest data for coronavirus, 
			and for news and weather if those parameters were ticekd

		announce(sched_alarm)
			announce the alarm via tts- also check if the alarm has been cancelled



Author:
Harry Collins

Github repository:
https://github.com/harry-kav/covid_daily_brief/

License and copyright:
© Harry Collins
Licensed under the MIT License(LICENSE)


		

