import urllib
import urllib2
from bs4 import BeautifulSoup
# import BeatifulSoup
import pprint

def get_url(textToSearch):
	textToSearch = "shape of you"
	query = urllib.quote(textToSearch)
	url = "https://www.youtube.com/results?search_query=" + query
	response = urllib2.urlopen(url)
	html = response.read()


	soup = BeautifulSoup(html)
	# for vid in soup.findAll(attrs={'class':'yt-uix-tile-link'}):
	#     print 'https://www.youtube.com' + vid['href']

	vid = soup.findAll(attrs={'class':'yt-uix-tile-link'})[:4]


	return ('https://www.youtube.com' + vid[0]['href'])

if __name__ == "__main__":
	get_url("shape of you")
