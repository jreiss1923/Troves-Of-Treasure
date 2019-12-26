import requests
import schedule
import mysql.connector
import datetime
import time

headers = {
    "Accept": "application/json",
    "Authorization": "bearer Z53dHTfmNTrZBij1Uc6LFvWJB2WU3jkrJRtonAR82G1m48246YvgdyrYtHaf0GVS6UZ_O9Gz4_SBkPWS3pNguvMF8P9q3T95-diC9SJObmN-9o9pxcEBo0LdHdFWx1nPrN4M8m0hYeKXZkZvb5W9_BYtV0q46xanbwVgi3ZtHsIHkvFloLG8yWg4f-eLYIiuJXKZZkuSHdzoX-HGNHyrrWnSk_WhwB_cejVp1SKAudzcQV5-MB-gimuSj0Iqck981BXGU3i5xUj62snOEFewM8Ma6T3-K_hwEsnp0mDedB9CiDCiLNC0sxyYxZBpkDmei0BaaQ"
}

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="Bigbrain2@",
    database="troves_of_treasure",
)

mycursor = mydb.cursor()

current_user_table = 0
current_user = ""

def bearer_token(PUBLIC_KEY, PRIVATE_KEY):
    bearer_headers = {
        'app': 'application/x-www-form-urlencoded',
    }

    data = 'grant_type=client_credentials&client_id=' + PUBLIC_KEY + '&client_secret=' + PRIVATE_KEY

    response = requests.post('https://api.tcgplayer.com/token', headers=bearer_headers, data=data).json()
    print(response)

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

def get_card_prices_no_comma(resultString):
    return get_card_prices(resultString + ",")

def card_foiling(resultString):
    response = requests.get("http://api.tcgplayer.com/v1.32.0/pricing/product/" + resultString[:len(resultString) - 1], headers=headers).json()
    foiled = []
    for i in response["results"]:
        if(i["subTypeName"] == "Normal"):
            foiled.append(False)
        else:
            foiled.append(True)

    return foiled

def card_foiling_no_comma(resultString):
    return card_foiling(resultString + ",")

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


#add card to current portfolio
def add_card(card_id, foiled, num_cards):
    mycursor.execute("insert into portfolio_card_assc(portfolio_id, card_id, card_count, foiled) values(" + str(current_user_table) + "," + str(card_id) + "," + str(num_cards) + "," + str(foiled) + ")")
    mydb.commit()


#updating portfolio function that runs daily
def update_portfolios_for_all_users():
    mycursor.execute("select username from user_info")
    usernames = mycursor.fetchall()

    for username in usernames:
        update_portfolios(username[0])

#update portfolio for one user
def update_portfolios(username):
    mycursor.execute("select id from portfolio where user_name = '" + username + "'")
    portfolio_ids = mycursor.fetchall()

    list_of_ids = []

    for x in portfolio_ids:
        list_of_ids.append(x[0])

    portfolio_prices = {}
    for id in list_of_ids:
        mycursor.execute("select card_id, card_count, foiled from portfolio_card_assc where portfolio_id = " + str(id))
        portfolio_prices[id] = mycursor.fetchall()

    total_prices = get_portfolio_prices(portfolio_prices)
    for key in total_prices:
        today = datetime.datetime.today()
        today_formatted = today.strftime('%Y-%m-%d')
        mycursor.execute("insert into date_price_info(date_of_price, price, portfolio_id) values('" + today_formatted + "'," + str(total_prices[key]) + "," + str(key) + ")")
        mydb.commit()

#returns price data for portfolios
def get_portfolio_prices(cards):
    portfolio_prices = {}
    for key in cards:
        if len(cards[key]) != 0:
            price = 0
            for portfolio_tuple in cards[key]:
                if(portfolio_tuple[2] == 0):
                    correct_pos = card_foiling_no_comma(str(portfolio_tuple[0])).index(False)
                else:
                    correct_pos = card_foiling_no_comma(str(portfolio_tuple[0])).index(True)
                price += get_card_prices_no_comma(str(portfolio_tuple[0]))[correct_pos] * portfolio_tuple[1]
            portfolio_prices[key] = price

    return portfolio_prices

def login_or_signup(username, password):
    global current_user
    mycursor.execute("select * from user_info where username = '" + username + "' and password = md5('" + password + "')")
    results = mycursor.fetchall()
    if len(results) > 0:
        current_user = username
        print(current_user)
    else:
        response = input("The username or password was incorrect. Enter t to try again, or enter s to sign up.")
        if(response == "t"):
            start_function()
        elif(response == "s"):
            username = input("Please choose a username")
            password = input("Please choose a password")
            email = input("Please enter your email address")
            mycursor.execute("insert into user_info(username, password, email) values('" + username + "', md5('" + password + "'), '" + email + "')")
            mydb.commit()

def start_function():
    username = input("Please input your username")
    password = input("Please input your password")
    login_or_signup(username, password)

#update_portfolios("jreiss1923")
#update_portfolios_for_all_users()
#schedule.every().day.at("07:00").do(update_portfolios_for_all_users)

start_function()

#while True:
#    schedule.run_pending()
#    time.sleep(1)

