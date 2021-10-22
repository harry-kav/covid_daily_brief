from flask import Flask, render_template, Markup
from flask import request
import pyttsx3

from uk_covid19 import Cov19API

import json
import requests

from news_filter import get_news 
from weather_update import get_weather
from get_news_and_weather import get_data
from get_covid_info import generate_covid_news
from time_manager import hhmm_to_seconds, hours_to_minutes, current_time_hhmm, minutes_to_seconds

import logging

import time
import sched
from datetime import date, datetime


s = sched.scheduler(time.time, time.sleep)

engine = pyttsx3.init()

with open('config.json') as config_file:
	data = json.load(config_file)
    
weather_key = data["weather_key"]
news_key = data["news_key"]
location = data["location"]
notification_update_interval = data["notification_update_interval"]
clear_removed_notifications_interval = data["clear_removed_notifications_interval"]
check_alarms_interval = data["check_alarms_interval"]

alarms = []
alarm_schedule = []

news_notifications, weather_notifications = get_data()

notifications = []
notifications.extend(news_notifications)
notifications.extend(weather_notifications)
removed_notifications = []


app = Flask(__name__)

def update_notifications():
	'''
	update the list of notifications, also making sure not to add dismissed notifications back to the list
	'''
	global notifications, removed_notifications

	news_notifications, weather_notifications = get_data()

	notifications = []

	for notification in news_notifications:
		if notification not in removed_notifications:
			try:
				notifications.append(notification)

				logging.info("notification updated")
			except:
				logging.error("notification update failed")
				pass

	for notification in weather_notifications:
		if notification not in removed_notifications:
			try:
				notifications.append(notification)
				logging.info("notification updated")
			except:
				logging.error("notification update failed")
				pass

	s.enter(notification_update_interval, 1, update_notifications,)

def clear_removed_notifications():
	'''
	after a certain amount of time(specified in config), clear removed notifications
	'''
	global removed_notifications

	removed_notificatisons = []
	logging.info("cleared notifications")

	try:
		s.enter(clear_removed_notifications_interval, 1, clear_removed_notifications,) #empty the removed notifications every 30 mins
		logging.info("scheduled to clear removed notifications")
	except:
		logging.error("failed to schedule to clear removed notifications")
		pass

def cancel_and_close(cancelled_alarm, closed_notification):
	'''
	cancel alarms and close notifications upon user request
	'''
	global alarms, notifications, removed_notifications

	if cancelled_alarm:
		for alarm in alarms:
			if alarm['title'] == cancelled_alarm:
				alarms.remove(alarm)

	if closed_notification:

		removed_notifications.append(closed_notification)
		logging.info("notification added to removed_notifications")

		for notification in notifications:
			if notification['title'] == request.args.get("notif"):

				notifications.remove(notification)

def check_alarms():
	'''
	on an interval, remove any alarms that have already passed
	'''
	global alarms

	dt_today = datetime.today()  # Get timezone naive now
	today_seconds = dt_today.timestamp()

	for alarm in alarms:
		dt_alarm_day = datetime.strptime(alarm['time'], "%Y-%m-%d %H:%M")
		alarm_day_seconds = dt_alarm_day.timestamp()

		if alarm_day_seconds - today_seconds <= 0 and alarm['status'] == "announced":
			#if the alarm has already been announced, remove it
			alarms.remove(alarm)
		#elif alarm_day_seconds - today_seconds <= 0 and alarm['status'] == "unannounced":
		#	announce(alarm)

	s.enter(check_alarms_interval, 1, check_alarms,)


def check_alarm_file():
	'''
	this function checks the alarm file when the server starts, loading future alarms and deleting past alarms
	'''
	global alarms

	try:
		with open('alarms.json', 'r') as alarm_file:
			dt_today = datetime.today()  # Get timezone naive now
			today_seconds = dt_today.timestamp()


			#if the alarm's due time has not arrived and the alarm is not in the alarms list, add it
			for alarm in alarm_file:
				dt_alarm_day = datetime.strptime(alarm['time'], "%Y-%m-%d %H:%M")
				alarm_day_seconds = dt_alarm_day.timestamp()

				if alarm_day_seconds - today_seconds > 0:
					if alarm not in alarms:
						alarms.append(alarm)
						s.enter(alarm_day_seconds - today_seconds, 1, (alarm,))


		logging.info("extracted alarms from file")
	except:
		logging.error("failed to extract alarms from file")
		pass

update_notifications()
clear_removed_notifications()

check_alarm_file()
check_alarms()

@app.route('/')
@app.route('/index')
def index():
	'''
	the main page- setting the alarm is handled here
	'''

	#alarms

	s.run(blocking=False)

	global alarms, notifications

	news_info = ''
	weather_info = ''

	for alarm in alarms:
		if alarm['status'] == 'announced':
			alarms.remove(alarm)
	
	check_alarms()

	#check for closed alarms and notifications

	cancelled_alarm = request.args.get("alarm_item")

	closed_notification = request.args.get("notif")

	alarm_time = request.args.get("alarm")

	cancel_and_close(cancelled_alarm, closed_notification)

	#setting the alarm
	if alarm_time:
        #convert alarm_time to a delay
		alarm_hhmm = alarm_time[-5:-3] + ':' + alarm_time[-2:]
		delay = hhmm_to_seconds(alarm_hhmm) - hhmm_to_seconds(current_time_hhmm())

		if request.args.get("news"):
			news_info = 'News' #the news will feature in the alarm
		if request.args.get("weather"):
			weather_info = 'Weather'

		logging.info("checked parameters for alarm")

		alarm_title = request.args.get("two")
		if alarm_title:
			alarm_title = request.args.get("two")
			for alarm in alarms:
				#check for duplicate names
				if alarm['title'] == alarm_title:
					alarm_title = alarm['title'] + "(1)"

		logging.info("set title for alarm")
					

		# if the announcement string contains 'news' it will say the latest news- same for 'weather'
		alarm_time_formatted = alarm_time.replace("T"," ")
		dt_alarm_day = datetime.strptime(alarm_time_formatted, "%Y-%m-%d %H:%M")

		logging.info("formatted alarm time")

		announcement_string = "Update for: COVID-19-" + news_info + "-" + weather_info +" At " + str(alarm_time_formatted)

		logging.info("set announcement string")

		if str(date.today()) in str(alarm_time):

			try:
				alarms.append({"title": alarm_title, "content": announcement_string, "time": str(alarm_time_formatted), "status": "unannounced"})
				logging.info("added alarm to alarm list")
			except:
				logging.error("failed to add alarm to list")
		else:
			dt_today = datetime.today()  # Get timezone naive now
			today_seconds = dt_today.timestamp()

			alarm_day_seconds = dt_alarm_day.timestamp()

			delay = alarm_day_seconds - today_seconds


			alarms.append({"title": alarm_title, "content": announcement_string, "time": str(alarm_time_formatted), "status": "unannounced"})
			logging.info("added alarm to list")


		#delete any accidental duplicates
		for alarm in alarms:
			if alarm['title']+ "(1)" == alarm_title and alarm['content'] == announcement_string:
				alarms.remove(alarm)
				logging.info("alarm removed")

		for alarm in alarms:
			if alarm['title'] == alarm_title:

				s.enter(int(delay), 1, announce, (alarm,))
				logging.info("alarm scheduled")


	return render_template('covid_brief_template.html', title='COVID Daily Brief', notifications=notifications, alarms=alarms, image='clock.jpeg')

def get_alarm_information(info_string): #-> int:
	'''
	converts the information in the alarm to the latest data for coronavirus, 
	and for news and weather if those parameters were ticekd
	'''
	covid_news = generate_covid_news()
	news_headlines = []
	headline_string = ''
	weather_info = ['','']
	weather_string = ''
	news_data, weather_data = get_data()

	#if news was requested in the alarm give the top 3 headlines
	if 'news' in info_string.lower():
		i = 0
		while i < 3:
			try:
				news_headlines.append(news_data[i]['title'])
				logging.info("added headline to announcement")
			except:
				news_headlines.append('')
				logging.error("failed to add headline to announcement")
				pass
			i+=1

		headline_string = "- The top headlines are: "+ news_headlines[0] + ' - ' + news_headlines[1] + ' - ' + news_headlines[2]

	if 'weather' in info_string.lower():
		for data in weather_data:
			if data['title'].lower() == 'temperature':
				try:
					weather_info[1] = '- The temperature is '+ data['content']
					logging.info("added temp to announcement")
				except:
					logging.error("failed to add temp to announcement")
					pass
			if data['title'].lower() == 'description':
				try:
					weather_info[0] = '- The weather can be described as '+ data['content']
					logging.info("added weather description to announcement")
				except:
					logging.error("failed to add weather description to announcement")

		weather_string = weather_info[0] + weather_info[1] + ". "


	announcement_string = covid_news + weather_string + ". " + headline_string

	return announcement_string


def announce(sched_alarm):
	'''
	announce the alarm via tts- also check if the alarm has been cancelled
	'''
	alarm_still_scheduled = False
	global alarms
	for alarm in alarms:
		if alarm == sched_alarm and alarm["status"] == "unannounced":
			alarm_still_scheduled = True

	sched_alarm['status'] = "announced"

	if alarm_still_scheduled == True:

		try:
			engine.endLoop()
		except:
			logging.error('announcement failed')  # will not print anything
			pass
		full_announcement = get_alarm_information(sched_alarm['content'])

		try:
			engine.say(full_announcement)
			engine.runAndWait()
			engine.endLoop()

			logging.info("announcement completed")

			sched_alarm['status'] = "announced"
		except:
			pass
			logging.error("announcement failed")

		alarms.remove(sched_alarm)

		with open('alarms.json') as alarm_file:
			dt_today = datetime.today()  # Get timezone naive now
			today_seconds = dt_today.timestamp()


			#if the alarm's due time has not arrived and the alarm is not in the alarms list, add it
			for alarm in alarm_file:
				if alarm['title'] == sched_alarm['title']:
					alarm_file.remove(alarm)




if __name__ == '__main__':
		'''
		run the app
		'''
		app.run(debug=False)
		app.logger.info("init")


logging.basicConfig(filename='log.log', encoding='utf-8', level=logging.INFO)
logging.info("application started")