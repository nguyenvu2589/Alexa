import logging
from flask import Flask, render_template
from flask_ask import Ask, statement, question, convert_errors
# from getYoutubeUrl import get_url
import webbrowser
from distance_matrix import find_distance
from get_restaurant_location import get_3_store

app = Flask(__name__)
ask = Ask(app, "/")

log = logging.getLogger()
log.addHandler(logging.StreamHandler())
log.setLevel(logging.DEBUG)
logging.getLogger("flask_ask").setLevel(logging.DEBUG)


@ask.launch
def launch():
    return question("Supp! Sexy ! How can I help you ?")


@ask.intent("HelloIntent")
def hello(firstname):
	return statement(" Hello {}. Nice to meet you".format(firstname))

# Done !!!!!!!
@ask.intent("mathIntent", convert = {'firstnumber': int, 'secondnumber': int})
def simple_math(firstnumber, secondnumber,operand):
	answer = 0
	if convert_errors:
		return statement("I am not sure what is {}".format(preference))

	if str(operand) == "add" or str(operand) == "plus":
		answer = firstnumber + secondnumber
	elif str(operand) == "substract" or str(operand) == "minus":
		answer = firstnumber - secondnumber
	elif str(operand) == "multiply" or str(operand) == "time":
		answer = firstnumber * secondnumber
	elif str(operand) == "divide" or str(operand) == "divide by":
		answer = float(firstnumber / secondnumber)
	else:
		return statement("Can you said it again ?")
	if int(answer) < 10:
		return statement("Seriously!! Use your head. Ask me harder question ")
	return statement("{} {} {} is {}".format(firstnumber, operand,secondnumber, answer))

# DONE !!!!!! 
# @ask.intent("playMusic", convert = {'song': str})
# def play_music(song):
	
	print song, "This is song"
	url = get_url(song)
	webbrowser.open_new(url)
	return statement("playing {} on youtube".format(song))

# Done !!!!!!


@ask.intent("introIntent")
def introduction():
	msg = 'What is 2+2 or check work traffic or i want some asian food from denver or im hungry'
	return question(msg)

@ask.intent("checkTraffic", convert = {'destination': str})
def check_traffic(destination):
	if convert_errors:
		return statement("I am not sure what is {}".format(preference))

	distance, duration, status,stat = find_distance(destination)
	if status == 'OK':
		if (stat):
			msg = "Looking good! It takes {} to get to {}".format(duration,destination)
		else:
			msg = "There is some traffic. It takes {} to get to {}".format(duration,destination)
	return statement(msg)

################################
### STOP ####
@ask.intent("AMAZON.StopIntent")
def stop():
	return statement("Bye !")

##### Find food place base on yelp reference. 
##### Simple utterances: I want some ______ food from ______
##### Or i'm hungry / i want some food from _______ 
@ask.intent("yelpIntent" ,default = {'term': 'New American'}, convert = {'term': str, 'city': str})
def find_3_store_on_yelp(term,city):
	
	store = get_3_store(term, city)
	
	msg = "How about " + " ".join (', {}'.format(x) for x in store) + "?"
	return statement(msg)


if __name__ == '__main__':
    app.run(debug=True)


# FEATURE : 
# 1. Say hi to ____
# 2. check ___school/work traffic
# 3. Simple math : what is 2+2 
# 4. im hungry for some __typeOfFood food in city ____cityName


