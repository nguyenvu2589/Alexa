import logging
from flask import Flask, render_template
from flask_ask import Ask, statement, question, session, convert_errors
from cocktail_finder import drink_lookup, random_genenrate_drink, data_stripping,msg_convert



app = Flask(__name__)
ask = Ask(app, "/")

log = logging.getLogger()
log.addHandler(logging.StreamHandler())
log.setLevel(logging.DEBUG)
logging.getLogger("flask_ask").setLevel(logging.DEBUG)


@ask.launch
def launch():
    return question("How can I help you ?")


@ask.intent("findDrinkIntent", default = {'drinkName':None }, convert= {'drinkName': str })
def find_drink(drinkName):

	#### Random drinks:  suggest 3 drinks
	if (drinkName is None):
		result = random_genenrate_drink()
		session.attributes['answer'] = result[0]
		return question(result[1])

	#### Actual request 
	else:
		# find the drink
		result = drink_lookup('drinks',drinkName)
		session.attributes['answer'] = result[0]

		return question(result[1])

# second steps from picking


### ADD check for list index range 
### try catch ... or whatever
@ask.intent("findDrinksecondIntent", convert= {'option': str })
def pick_from_previous_opt(option):
	search_term = 'drinks'
	drink_list = session.attributes['answer']
	try:
		if option == 'first' or option == 'one' or option == '1st':
			return statement ('So  {}'.format(''.join(msg_convert(drink_list[0],search_term)).encode('utf-8').strip()))
		elif option == 'second' or option == 'two' or option == '2nd':
			return statement ('So  {}'.format(''.join(msg_convert(drink_list[1],search_term)).encode('utf-8').strip()))
		elif option == 'third' or option == 'three' or option == '3rd':
			return statement ('So  {}'.format(''.join(msg_convert(drink_list[2],search_term)).encode('utf-8').strip()))
		elif option == 'forth' or option == 'four' or option == '4th':
			return statement ('So  {}'.format(''.join(msg_convert(drink_list[3],search_term)).encode('utf-8').strip()))
		elif option == 'fifth' or option == 'five' or option == '5th':
			return statement ('So  {}'.format(''.join(msg_convert(drink_list[4],search_term)).encode('utf-8').strip()))
		else:
			return question('Please pick again, {} is not an available option'.format(option) )
	except: 
		return question('Please pick again, {} is not an available option'.format(option) )

if __name__ == '__main__':
    app.run(debug=True)



