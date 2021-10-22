import time


def hhmm_to_seconds( hhmm: str ) -> int:
	'''
	converts hhmm into seconds
	'''
	if len(hhmm.split(':')) != 2:
		print('Incorrect format. Argument must be formatted as HH:MM')
		return None
	return minutes_to_seconds(hours_to_minutes(hhmm.split(':')[0])) + \
		minutes_to_seconds(hhmm.split(':')[1])

def hours_to_minutes( hours: str ) -> int:
    """Converts hours to minutes"""
    return int(hours)*60

def minutes_to_seconds( minutes: str ) -> int:
      """Converts minutes to seconds"""
      return int(minutes)*60

def current_time_hhmm():
	'''
	returns the current time
	'''
	return str(time.gmtime().tm_hour) + ":" + str(time.gmtime().tm_min)
