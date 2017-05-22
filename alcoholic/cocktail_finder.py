import unirest
import pprint
import sys
from random import randint
from random import random



#### one long ass function
# should break it down into smaller function 
# bad practice.
def data_stripping(search_term,drink):
	result = {}
	taste= []
	ingredient = []
	instruction = []
	
	newMsg = ''
	# try:
	if search_term == 'drinks':
		newDescription = drink['descriptionPlain']
		#parse ingredient from big list bring to smaller array
		# replace - with space. 
		# get the make instruction and store in instruction. 
		for item in drink['ingredients']:
			ingredient.append(item['id'].replace('-', ' '))
			instruction.append(item['textPlain'])

		# pull taste from big data and store in smaller array.
		for item in drink['tastes']:
			taste.append(item['text'])

		### if instruction just have add all ingredients
		### replace it with all ingredient
		if "add all ingredients" in drink['descriptionPlain'].lower():
			newMsg = ', '.join([x for x in instruction])
			newDescription = drink['descriptionPlain'].replace('all ingredients',newMsg)

		# convert instruction, add quantity into string
		# convert that into instruction message from description
		for i in range (len(ingredient)):
			if ingredient[i].lower() in drink['descriptionPlain'].lower():
				newDescription = newDescription.replace(ingredient[i],instruction[i])

		result = {
			'name' : drink['name'],
			'instruction': newDescription,
			'ingredients': ingredient,
			'tastes': taste,
			'rating': drink['rating']
		}
	elif search_term == 'ingredients':
		result = {
			'name' : drink['name'],
			'descriptionPlain': drink['description'],
			'type': drink['type'],
		}
	else:
		print "Result is null !!!!"
		result = {}
	# except Exception, e:
	# 	print str(e)
		# result = {}
		# pass
	return result

#### Done !!!!
def drink_lookup(search_term,search_name):
	result_list = []
	# try: 
		# search data 
	url ='http://addb.absolutdrinks.com/quickSearch/{}/{}/?apiKey={}'.format(search_term,search_name,addb_key) 
	result = unirest.get(url)

	for item in result.body['result']:

		if search_name.lower() in item['name'].lower() :
			result_list.append(data_stripping(search_term,item))
	
	# process
	# didnt find 
	if len(result_list) <1 :
		return (None,'Sorry I cannot find anything matches with {}'.format(search_name))
	elif len(result_list) == 1:
		return (result_list,'So  {}'.format(', \n'.join([msg_convert(x,search_term) for x in result_list]).encode('utf-8').strip()))
	elif len(result_list) < 6:
		return (result_list,'I found: {}. Which one do you want to know more about?'.format(' ,'.join([x['name'] for x in result_list]).encode('utf-8').strip()))
	else:
		return (result_list,'I found: {} and few more. Which one do you want to know more about?'.format(' ,'.join([x['name'] for x in result_list[:5]]).encode('utf-8').strip()))
	# except Exception, e:
	# 	print str(e)
		return (None, 'Please try again. There is something wrong with the server.')

### Done !!!!

def random_genenrate_drink():
	result_list = []
	start = set([randint(1, 3636) for _ in range(3)])
	try:
		for i in start:
			url ='http://addb.absolutdrinks.com/drinks/?apiKey={}&start={}&pageSize=1'.format(addb_key,i) 
			result = unirest.get(url)
			result_list.append(data_stripping('drinks',result.body['result'][0]))
	except Exception, e:
		print str(e) 
		return (None, 'Please try again. There is something wrong with the server.')

	return (result_list, 'How about {}'.format(' , or '.join([x['name'] for x in result_list]).encode('utf-8').strip()))

######### prepare message
def msg_convert(result,search_term):
	pprint.pprint(result)
	print "This is result"
	if search_term == 'drinks':
		msg = '{} has {} and it tastes like {}'.format(result['name'], 
						" ,".join([ x for x in result['ingredients']]),
						" ,".join([ x for x in result['tastes']]))
	elif search_term == 'ingredients':
		if result['type'] == 'others':
			msg = '{}: \n {}'.format(result['name'],result['descriptionPlain'])
		else:
			msg = '{} is a type of {}. And {} '.format(result['name'], result['type'], result['descriptionPlain'])
	return msg



def test_function (search_term,search_name):
	result_list = []
	# try: 
		# search data 
	url ='http://addb.absolutdrinks.com/quickSearch/{}/{}/?apiKey={}'.format(search_term,search_name,addb_key) 
	result = unirest.get(url)

	for item in result.body['result']:
		if search_name.lower() in item['name'].lower() :
			result_list.append(data_stripping(search_term,item))

	pprint.pprint (result_list[0])
	print ('So  {}'.format(''.join(msg_convert(result_list[0],search_term)).encode('utf-8').strip()))
	#return statement 

if __name__ == "__main__":

	# instruction
	# pass in type wanna search and name of liquor
	# function return a list 
	# [0] a full package
	# [1] complete message

	# TODO : 
	# problem lemon curd and lemon cu still be accepted
	# Solution : if 1 result return wanna make sure it match 100%
	# it might lower the accuracy of the program,

	a = drink_lookup('drinks',"the lemon drop")
	# b = drink_lookup('drinks',"Brainstorm")
	# print a
	# print a[0][0]['instruction'] # get instrcution
	# msg_convert(a[0])

	# a = random_genenrate_drink()
	# print len(a[0])
	# pprint.pprint (a[0])


