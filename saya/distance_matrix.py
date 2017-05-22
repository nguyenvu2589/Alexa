import os
import sys
import requests
import unirest
import pprint


google_api_key = ''
home = 'ADDRESS'
work = 'ADDRESS'
school = 'ADDRESS'
def check_status(des,distance, duration):
	distance = distance.split(' ')
	duration = duration.split(' ')
	dis = float(distance[0])
	dur = float(duration[0])
	if des == 'school' and dis < 21 :
		return True if dur < 35 else False
	elif des =='work' and dis < 33 :
		 return True if dur < 48 else False
	else:
		return False

def find_distance(des):
	if des == 'school':
		destination = school
	else:
		destination = work

	link = "https://maps.googleapis.com/maps/api/distancematrix/json?units=imperial&origins={}&destinations={}&key={}".format(home,destination,google_api_key)
	response = unirest.get(link)
	pprint.pprint (response.body)
	#pprint.pprint (response.body['rows'][0]['elements'][0]['duration']['text'])
	distance = response.body['rows'][0]['elements'][0]['distance']['text']
	duration = response.body['rows'][0]['elements'][0]['duration']['text']
	status = response.body['status']

	stat = check_status(des, distance, duration)
	return distance, duration, status, stat
if __name__ == "__main__":
	des = ''
  	find_distance(des)




  