
API_list = [
]


class UriSourceRetrievalAPI(object):
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


newAPI = UriSourceRetrievalAPI(
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


newAPI = UriSourceRetrievalAPI(
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