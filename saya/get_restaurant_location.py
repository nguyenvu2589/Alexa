
# Sample usage of the program:
# `python sample.py --term="bars" --location="San Francisco, CA"`

from urllib2 import HTTPError
from urllib import quote
from urllib import urlencode
import unirest
import argparse
import json
import pprint
import requests
import sys
import urllib
from random import randint

CLIENT_ID = ''
CLIENT_SECRET = ''


# API constants, you shouldn't have to change these.
API_HOST = 'https://api.yelp.com'
SEARCH_PATH = '/v3/businesses/search'
BUSINESS_PATH = '/v3/businesses/'  # Business ID will come after slash.
TOKEN_PATH = '/oauth2/token'
GRANT_TYPE = 'client_credentials'


# Defaults for our simple example.
DEFAULT_TERM = 'restaurant'
DEFAULT_LOCATION = 'Denver, CO'

google_key = ''

def obtain_bearer_token(host, path):
    
    url = '{0}{1}'.format(host, quote(path.encode('utf8')))
    assert CLIENT_ID, "Please supply your client_id."
    assert CLIENT_SECRET, "Please supply your client_secret."
    data = urlencode({
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
        'grant_type': GRANT_TYPE,
    })
    headers = {
        'content-type': 'application/x-www-form-urlencoded',
    }
    response = requests.request('POST', url, data=data, headers=headers)
    bearer_token = response.json()['access_token']
    return bearer_token


def request(host, path, bearer_token, url_params=None):
    url_params = url_params or {}
    url = '{0}{1}'.format(host, quote(path.encode('utf8')))
    headers = {
        'Authorization': 'Bearer %s' % bearer_token,
    }

    print(u'Querying {0} ...'.format(url))

    response = requests.request('GET', url, headers=headers, params=url_params)

    return response.json()


def search(bearer_token, term, latitude, longitude,city ):
    SEARCH_LIMIT = 10

    radius= '8000'
    open = True
    if city is None:
        url_params = {
            'term': term.replace(' ', '+'),
            'latitude': latitude.replace(' ', '+'),
            'longitude': longitude.replace(' ', '+'),
            'radius': radius.replace(' ', '+'),
            'price': '1,2,3',
            'limit': SEARCH_LIMIT,
            'open_now': open,

        }
    else :
        url_params = {
            'term': term.replace(' ', '+'),
            'location': city.replace(' ', '+'),
            'radius': radius.replace(' ', '+'),
            'price': '1,2,3',
            'limit': SEARCH_LIMIT,
            'open_now': open,

        }
    return request(API_HOST, SEARCH_PATH, bearer_token, url_params=url_params)


def get_business(bearer_token, business_id):

    business_path = BUSINESS_PATH + business_id

    return request(API_HOST, business_path, bearer_token)


def query_api(term, latitude, longitude,city ):
    store = set()
    bearer_token = obtain_bearer_token(API_HOST, TOKEN_PATH)
    response = search(bearer_token, term, latitude, longitude, city)
    businesses = response.get('businesses')
    if not businesses:
        print(u'No businesses for {0} in this area found.'.format(term))
        return

    business_id = 0

    #### check total restaurant found.
    #### max search is 10 but only want to return 3
    # print(u'{0} businesses found, querying business info ' \
    #     'for the top result "{1}" ...'.format(
    #         len(businesses), business_id))
    if len(businesses) > 0:
        business_name = businesses[0]['name']
        store.add(business_name)
        if len(businesses) > 1:
            numbers = [randint(1, len(businesses)) for _ in range(2)] 

            store.add(businesses[numbers[0]]['name'])
            try:
                store.add(businesses[numbers[1]]['name'])
            except IndexError:
                pass
    
    return store

    #### get more info from restaurant such as location, phone, reviews ...
    # for item in businesses:
    #     business_id = item['id']
    #     response = get_business(bearer_token, business_id)
    #     # print response['name']
    #     # store.append(response['name'])
    #     print(u'Result for business "{0}" found:'.format(business_id))
    #     pprint.pprint(response, indent=2)

def get_current():
    link = 'https://www.googleapis.com/geolocation/v1/geolocate?key={}'.format(google_key)
    response = unirest.post(link)
    if response.status == '200':
        return (response.body['location'])
    else:
        return ('Aurora')

def get_3_store(place,city):
    term = place + ' restaurant'
    #### get current location
    location = get_current()
    latitude = str(location['lat'])
    longitude = str(location['lng'])

    #### search for restaurant
    try:
        return query_api(term, latitude, longitude,city)
    except HTTPError as error:
        sys.exit(
            'Encountered HTTP error {0} on {1}:\n {2}\nAbort program.'.format(
                error.code,
                error.url,
                error.read(),
            )
        )


if __name__ == '__main__':
    get_3_store('asian fusion', None)
    # get_current()