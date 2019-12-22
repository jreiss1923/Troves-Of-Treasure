import requests
import sys
import schedule
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

def search_card(cardString):
    params = {
        "productName": cardString
    }
    response = requests.get("http://api.tcgplayer.com/v1.32.0/catalog/products", headers=headers, params=params).json()
    return response

def card_to_id(response):
    s = ""
    for i in range(len(response["results"])):
        s += str(response["results"][i]["productId"]) + ","

    return s

def get_card_prices(resultString):
    response = requests.get("http://api.tcgplayer.com/v1.32.0/pricing/product/" + resultString[:len(resultString) - 1], headers=headers).json()
    prices = []
    for i in response["results"]:
        if(i["marketPrice"] != None):
            prices.append(float(i["marketPrice"]))
        else:
            prices.append(None)

    return prices

def card_foiling(resultString):
    response = requests.get("http://api.tcgplayer.com/v1.32.0/pricing/product/" + resultString[:len(resultString) - 1], headers=headers).json()
    foiled = []
    for i in response["results"]:
        if(i["subTypeName"] == "Normal"):
            foiled.append(False)
        else:
            foiled.append(True)

    return foiled


def low_price(prices):
    x = sys.maxsize
    for price in prices:
        if x > price:
            x = price

    return x

def get_user(username, password):
    global current_user_table
    mycursor.execute("select * from user_info where username='" + username + "' and password=md5('" + password + "')")
    user_value = mycursor.fetchall()
    if(len(user_value) > 0):
        mycursor.execute("select * from portfolio where user_name='" + username + "'")
        all_portfolios = mycursor.fetchall()
        current_user_table = all_portfolios[0][1]
        return True
    return False

def create_portfolio(username, name):
    mycursor.execute("insert into portfolio(name, user_name) values ('" + name + "', '" + username + "')")
    mydb.commit()

def change_portfolio(username, name):
    global current_user_table
    if(name != ""):
        mycursor.execute("select * from portfolio where user_name='" + username + "' and name='" + name + "'")
        all_portfolios = mycursor.fetchall()
        for x in all_portfolios:
            mycursor.execute("select count(*) from portfolio_card_assc where portfolio_id=" + str(x[1]))
            portfolio_count = mycursor.fetchall()[0][0]
            print("portfolio id " + str(x[1]) + " has " + str(portfolio_count) + " entries and name " + name)
    else:
        mycursor.execute("select * from portfolio where user_name='" + username + "'")
        all_portfolios = mycursor.fetchall()
        for x in all_portfolios:
            mycursor.execute("select count(*) from portfolio_card_assc where portfolio_id=" + str(x[1]))
            portfolio_count = mycursor.fetchall()[0][0]
            mycursor.execute("select name from portfolio where id=" + str(x[1]))
            portfolio_name = mycursor.fetchall()[0][0]
            print(portfolio_name)
            print("portfolio id " + str(x[1]) + " has " + str(portfolio_count) + " entries and name " + portfolio_name)
    chosen_id = input("Which portfolio id would you like to use?")
    current_user_table = int(chosen_id)

def get_card_info(card_name):
    card_info = search_card(card_name)
    s = ""
    for x in card_info['results']:
        s += str(x['groupId']) + ","
    set_arr = get_group_names(s)
    id_arr = card_to_id(card_info).split(",")
    price_arr = get_card_prices(card_to_id(card_info))
    foiled_arr = card_foiling(card_to_id(card_info))

    for y in range(0, len(price_arr), 1):
        if(price_arr[y] != None):
            if(foiled_arr[y] == True):
                print(set_arr[y // 2] + " " + id_arr[y // 2] + " " + str(price_arr[y]) + " foiled")
            else:
                print(set_arr[y//2] + " " + id_arr[y//2] + " " + str(price_arr[y]) + " nonfoiled")

def get_group_names(groupIdStr):
    group_ids = groupIdStr.split(",")
    response = requests.get("http://api.tcgplayer.com/v1.32.0/catalog/groups/" + str(groupIdStr), headers=headers).json()
    set_arr = [None] * len(group_ids)
    for x in response['results']:
        set_arr[group_ids.index(str(x['groupId']))] = x['name']
    return set_arr

def add_card(card_id, foiled, num_cards):
    mycursor.execute("insert into portfolio_card_assc(portfolio_id, card_id, card_count, foiled) values(" + str(current_user_table) + "," + str(card_id) + "," + str(num_cards) + "," + str(foiled) + ")")
    mydb.commit()

change_portfolio("jreiss1923", "")
get_card_info("Noble Hierarch")
add_card(28579, True, 4)
#def bearer_token(PUBLIC_KEY, PRIVATE_KEY):
    # bearer_headers = {
    #    'app': 'application/x-www-form-urlencoded',
    # }

    # data = 'grant_type=client_credentials&client_id=' + PUBLIC_KEY + '&client_secret=' + PRIVATE_KEY

    # response = requests.post('https://api.tcgplayer.com/token', headers=bearer_headers, data=data)
    # bearer_token = response[whatever i have to get]

