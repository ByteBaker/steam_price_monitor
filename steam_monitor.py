from bs4 import BeautifulSoup
import requests
from time import sleep
import json
from os import system
from api_library import API_list

								
# Change below variables as per need.

POSITION = 1					# Item at this position in hash_names will be monitored
CURRENCY = 'INR'
APP_ID = '730'					# 730 for CSGO

hash_names = [
	'USP-S | Cortex (Minimal Wear)',								#0
	'M4A1-S | Golden Coil (Minimal Wear)',							#1
	'AK-47 | Neon Rider (Minimal Wear)',							#2
	'Desert Eagle | Light Rail (Minimal Wear)',						#3
	'StatTrak™ Desert Eagle | Light Rail (Minimal Wear)', 			#4
]

# Modify only the variables above
# DO NOT MESS WITH THE CODE BELOW!

localhost_header = {
	'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'
}

total_attempts = 0											# Keeps track of total number of requests to steam
USD_to_LOCAL_API_URL = 'https://api.exchangeratesapi.io/latest?base=USD&symbols=' + CURRENCY		# returns the current price in Local Currency
search_url = 'https://steamcommunity.com/market/search?appid=' + APP_ID + '&q='

USDtoLOCAL_API_response = requests.get(USD_to_LOCAL_API_URL)
JSON_response = json.loads(USDtoLOCAL_API_response.text)
USDtoLOCAL_rate = JSON_response.get('rates').get(CURRENCY)

system('title Steam Monitor Script')
SEARCH_INDEX = POSITION - 1
print("\n------------------ Steam Price Monitor by ByteBaker ------------------")
print("---------- https://github.com/ByteBaker/steam_price_monitor ----------\n")

def get_price_on_steam(search_term=None, index=0, use_localhost=False):
	if not use_localhost:
		API_list[index].data[API_list[index].key] = search_url+search_term
		try:
			page_response = requests.post(API_list[index].URL, data=API_list[index].data, headers=API_list[index].headers, timeout=5)
		except KeyboardInterrupt:
			choice = input("Do you want to exit (y/n):")
			if choice == 'y':
				exit(0)
			else:
				pass
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
		except:
			return 0.0	

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

	return price*USDtoLOCAL_rate


while True:
	try:
		for i in range(len(API_list)):
			new_price = get_price_on_steam(search_term=hash_names[SEARCH_INDEX], index=i, use_localhost=False)
			if new_price == 0.0:
				print("Too many requests! Changing Mode...")
			else:
				local_price = "{:.2f}".format(new_price)
				total_attempts += 1
				print('Attempt:', total_attempts, '|', hash_names[SEARCH_INDEX], 'Price :', CURRENCY, local_price)
			sleep(5)

		new_price = get_price_on_steam(search_term=hash_names[SEARCH_INDEX], use_localhost=True)
		if new_price == 0.0:
			print("Too many requests! Changing Mode...")
		else:
			local_price = "{:.2f}".format(new_price)
			total_attempts += 1
			print('Attempt:', total_attempts, '|', hash_names[SEARCH_INDEX], 'Price :', CURRENCY, local_price)
		sleep(5)

	except KeyboardInterrupt:
		choice = input("Do you want to exit (y/n):")
		if choice == 'y':
			exit(0)
		else:
			continue