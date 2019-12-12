import requests

headers = {
    "Accept": "application/json",
    "Authorization": "bearer JijuljIEFOaaV2CIU7cpXc_uODdf0euxYhOGolYFlY8Ivqiz4nbnGcHZxwSbvav10ElZx7pQfvO4DnZ0qD1UnL3xc5l2uQP3xUBGp4U_Av35LhZlUH3S2sqVUN5XSxU5g6EhjAHyZPT1WqsXD_bet7vD48la6cLB0E-verohCqtERHVjXFQtFRut_gXmJrmESYP9vq4WH5sTPWbactvev7AvV2g7SF6hGix-yhXxR2SbgVyAWmTtsrlKM52mEB3SZaGVvdaEAbKGV-AtXmjpjymAsgvlYErcraSWiqOcwHQOj6rGKCprIRIs_pIw8-4cw9C1_A"
}

def search_card_prices(cardString):
    params = {
        "productName": cardString
    }
    product_prices = []
    response = requests.get("http://api.tcgplayer.com/v1.32.0/catalog/products", headers=headers, params=params).json()
    for i in range(len(response["results"])):
        product_prices.append(response["results"][i]["productId"])

def price_of_card(cardId):
    print("hi")

#def bearer_token(PUBLIC_KEY, PRIVATE_KEY):
    # bearer_headers = {
    #    'app': 'application/x-www-form-urlencoded',
    # }

    # data = 'grant_type=client_credentials&client_id=' + PUBLIC_KEY + '&client_secret=' + PRIVATE_KEY

    # response = requests.post('https://api.tcgplayer.com/token', headers=bearer_headers, data=data)
    # bearer_token = response[whatever i have to get]

search_card_prices("noble hierarch")