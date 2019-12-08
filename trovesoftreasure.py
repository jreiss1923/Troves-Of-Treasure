import requests

headers = {
    "Accept": "application/json",
    "Authorization": "bearer JijuljIEFOaaV2CIU7cpXc_uODdf0euxYhOGolYFlY8Ivqiz4nbnGcHZxwSbvav10ElZx7pQfvO4DnZ0qD1UnL3xc5l2uQP3xUBGp4U_Av35LhZlUH3S2sqVUN5XSxU5g6EhjAHyZPT1WqsXD_bet7vD48la6cLB0E-verohCqtERHVjXFQtFRut_gXmJrmESYP9vq4WH5sTPWbactvev7AvV2g7SF6hGix-yhXxR2SbgVyAWmTtsrlKM52mEB3SZaGVvdaEAbKGV-AtXmjpjymAsgvlYErcraSWiqOcwHQOj6rGKCprIRIs_pIw8-4cw9C1_A"
}

#headers = {
#    'app': 'application/x-www-form-urlencoded',
#}

data = 'grant_type=client_credentials&client_id=' + PUBLIC_KEY + '&client_secret=' + PRIVATE_KEY
bearer_token = "JijuljIEFOaaV2CIU7cpXc_uODdf0euxYhOGolYFlY8Ivqiz4nbnGcHZxwSbvav10ElZx7pQfvO4DnZ0qD1UnL3xc5l2uQP3xUBGp4U_Av35LhZlUH3S2sqVUN5XSxU5g6EhjAHyZPT1WqsXD_bet7vD48la6cLB0E-verohCqtERHVjXFQtFRut_gXmJrmESYP9vq4WH5sTPWbactvev7AvV2g7SF6hGix-yhXxR2SbgVyAWmTtsrlKM52mEB3SZaGVvdaEAbKGV-AtXmjpjymAsgvlYErcraSWiqOcwHQOj6rGKCprIRIs_pIw8-4cw9C1_A"

#response = requests.post('https://api.tcgplayer.com/token', headers=headers, data=data)
response = requests.get("http://api.tcgplayer.com/v1.32.0/catalog/categories", headers=headers)

print(response.text)
