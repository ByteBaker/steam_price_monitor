from bs4 import BeautifulSoup
import requests
from time import sleep
import json
from os import system


localhost_header = {
'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'
}

total_attempts = 0											# Keeps track of total number of requests to the server
USD_to_INR_API_URL = 'https://api.exchangeratesapi.io/latest?symbols=INR&base=USD'		# returns the current price in Indian Rupee
search_url = 'https://steamcommunity.com/market/search?appid=730&q='

USDtoINR_API_response = requests.get(USD_to_INR_API_URL)
JSON_response = json.loads(USDtoINR_API_response.text)
USDtoINR_rate = JSON_response.get('rates').get('INR')

hash_names = [
'USP-S | Cortex (Minimal Wear)',							#0
'M4A1-S | Golden Coil (Minimal Wear)',						#1
'AK-47 | Neon Rider (Minimal Wear)',						#2
'Desert Eagle | Light Rail (Minimal Wear)',					#3
'StatTrak™ Desert Eagle | Light Rail (Minimal Wear)', 		#4
]

SEARCH_INDEX = 4 											# Item at this index in hash_names will be monitored

API_list = [
]

system('title Steam Monitor Script')

class UriSourceRetrivalAPI(object):
	"""class to store a web API form data and headers"""
	URL = None
	headers = None
	data = None
	key = None
	uses_json = None
	json_key = None

	def __init__(self, url=None, headers=None, data=None, key=None, uses_json=False, json_key=None):
		self.URL = url
		self.headers = headers
		self.data = data
		self.key = key
		self.uses_json = uses_json
		self.json_key = json_key


newAPI = UriSourceRetrivalAPI(
	url = 'https://eternitech.com/wp-admin/admin-ajax.php',
	headers = {
		'accept': 'application/x-www-form-urlencoded; charset=UTF-8',
		'content-type': 'application/x-www-form-urlencoded',
		'dnt': '1',
		'origin': 'https://eternitech.com',
		'referer': 'https://eternitech.com/online_tools/source-code-viewer/',
		'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36'
		},
	data = {
		'x': None,
		'a': '2',
		'y': '',
		'action': 'ws_ajax',
		'id':'52'
	},
	key = 'x',
	uses_json = True,
	json_key = 'data'
	)
API_list.append(newAPI)


newAPI = UriSourceRetrivalAPI(
	url = 'https://codebeautify.com/URLService',
	headers = {
		'accept': 'text/plain, */*; q=0.01',
		'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
		'dnt': '1',
		'origin': 'https://codebeautify.org',
		'referer': 'https://codebeautify.org/source-code-viewer',
		'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36'
		},
	data = {
		'path': None
	}, 
	key = 'path',
	uses_json = False,
	json_key = None
	)
API_list.append(newAPI)


def get_price_on_steam(search_term=None, index=0, use_localhost=False):
	if not use_localhost:
		API_list[index].data[API_list[index].key] = search_url+search_term
		try:
			page_response = requests.post(API_list[index].URL, data=API_list[index].data, headers=API_list[index].headers, timeout=5)
		except:
			return 0.0	

		if API_list[index].uses_json:
			page_content = BeautifulSoup(json.loads(page_response.text).get(API_list[index].json_key), "lxml")
		else:
			page_content = BeautifulSoup(page_response.text, "lxml")

	else:
		try:
			page_response = requests.get(search_url+search_term, headers=localhost_header, timeout=5)
			page_content = BeautifulSoup(page_response.text, "lxml")
		except KeyboardInterrupt:
			choice = input("Do you want to exit (y/n):")
			if choice == 'y':
				exit(0)
			else:
				pass

	divs = page_content.find_all('div')
	price = 0
	for div in divs:
		if div.get('data-hash-name') == search_term:
			spans = div.find_all('span')
			for span in spans:
				if span.get('class')[0] == 'normal_price':
					price = float(span.text.split()[0].split('$')[1])
					break
			break

	return price*USDtoINR_rate


while True:
	try:
		for i in range(len(API_list)):
			total_attempts += 1
			new_price = get_price_on_steam(search_term=hash_names[SEARCH_INDEX], index=i, use_localhost=False)
			if new_price == 0.0:
				print("Too many requests! Changing Mode...")
				sleep(5)
				continue
			else:
				rupee_price = "{:.2f}".format(new_price)
				print('Attempt:', total_attempts, '|', hash_names[SEARCH_INDEX], 'Price : ₹'+rupee_price)
			sleep(5)

		total_attempts += 1
		new_price = get_price_on_steam(search_term=hash_names[SEARCH_INDEX], use_localhost=True)
		if new_price == 0.0:
			print("Too many requests! Changing Mode...")
			sleep(5)
			continue
		else:
			rupee_price = "{:.2f}".format(new_price)
			print('Attempt:', total_attempts, '|', hash_names[SEARCH_INDEX], 'Price : ₹'+rupee_price)
			sleep(5)
	except KeyboardInterrupt:
		choice = input("Do you want to exit (y/n):")
		if choice == 'y':
			exit(0)
		else:
			continue