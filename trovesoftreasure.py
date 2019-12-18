import requests
import sys
import json
import mysql.connector

headers = {
    "Accept": "application/json",
    "Authorization": "bearer JijuljIEFOaaV2CIU7cpXc_uODdf0euxYhOGolYFlY8Ivqiz4nbnGcHZxwSbvav10ElZx7pQfvO4DnZ0qD1UnL3xc5l2uQP3xUBGp4U_Av35LhZlUH3S2sqVUN5XSxU5g6EhjAHyZPT1WqsXD_bet7vD48la6cLB0E-verohCqtERHVjXFQtFRut_gXmJrmESYP9vq4WH5sTPWbactvev7AvV2g7SF6hGix-yhXxR2SbgVyAWmTtsrlKM52mEB3SZaGVvdaEAbKGV-AtXmjpjymAsgvlYErcraSWiqOcwHQOj6rGKCprIRIs_pIw8-4cw9C1_A"
}

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="Bigbrain2@",
    database="troves_of_treasure",
)

mycursor = mydb.cursor()

current_user_table = 0

def search_card_prices(cardString):
    params = {
        "productName": cardString
    }
    s = ""
    response = requests.get("http://api.tcgplayer.com/v1.32.0/catalog/products", headers=headers, params=params).json()
    for i in range(len(response["results"])):
        s += str(response["results"][i]["productId"]) + ","

    response = requests.get("http://api.tcgplayer.com/v1.32.0/pricing/product/" + s[:len(s) - 1], headers=headers).json()
    prices = []
    for i in range(len(response["results"])):
        if(json.dumps(response["results"][i]["marketPrice"]) != 'null'):
            prices.append(float(json.dumps(response["results"][i]["marketPrice"])))

    return low_price(prices)

def low_price(prices):
    x = sys.maxsize
    for price in prices:
        if x > price:
            x = price

    return x

def get_user(username, password):
    global current_user_table
    mycursor.execute("select * from user_info where username='" + username + "' and password='" + password + "'")
    user_value = mycursor.fetchall()
    if(len(user_value) == 0):
        mycursor.execute("select * from portfolio where user_name='jreiss1923'")
        all_portfolios = mycursor.fetchall()
        current_user_table = all_portfolios[0][1]
        return True
    return False

print(get_user("jreiss1923", "Bigbrain2@"))
print(current_user_table)


#def bearer_token(PUBLIC_KEY, PRIVATE_KEY):
    # bearer_headers = {
    #    'app': 'application/x-www-form-urlencoded',
    # }

    # data = 'grant_type=client_credentials&client_id=' + PUBLIC_KEY + '&client_secret=' + PRIVATE_KEY

    # response = requests.post('https://api.tcgplayer.com/token', headers=bearer_headers, data=data)
    # bearer_token = response[whatever i have to get]

