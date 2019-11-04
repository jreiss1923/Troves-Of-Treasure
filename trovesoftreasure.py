import requests

headers = {
    'header': 'application/x-www-form-urlencoded'
}

header = "http://application/x-www-form-urlencoded"
PUBLIC_KEY = '682B81DB-4A64-4381-91B5-CD9A26D34D26'
PRIVATE_KEY = "69BDD4FE-FE4F-4A2C-964F-BC23B73FD746"

data = 'grant_type=client_credentials&client_id=' + PUBLIC_KEY + '&client_secret=' + PRIVATE_KEY

response = requests.post('https://api.tcgplayer.token', headers=headers, data = data)

print(response.text)
