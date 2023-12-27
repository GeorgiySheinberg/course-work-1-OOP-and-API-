import requests
from urllib.parse import urlencode
vk_url = 'https://oauth.vk.com/authorize'
params = {
    'client_id': 51794519,
    "redirect_uri": '',
    'display': 'page',
    'scope': 'photos',
    'response_type': 'token'
}
oath_url = f'{vk_url}?{urlencode(params)}'
print(oath_url)
response = requests.get(f'{vk_url}?{urlencode(params)}')
