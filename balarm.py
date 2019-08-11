import requests
import time
from win10toast import ToastNotifier


toaster = ToastNotifier()


print(' Welcome in Balarm. Bitcoin notification app for windows')
print('*********************************************************')
print("")
print('Choose how often do you want to get notification from Balarm')
notification_time = int(input("Time in sec: "))
print("")
print('Choose which currency you want to display')
print('1. CZK 2. USD 3. CZK+USD')
currency = int(input("Type 1 or 2 or 3: "))


# This function will return float number which will represent price of 1 btc in USD.
def get_bitcoin_rate_usd():

    r = requests.get('https://api.coindesk.com/v1/bpi/currentprice.json')
    bitcoin_rate_usd = r.json()['bpi']['USD']['rate'].replace(',', '')
    return round(float(bitcoin_rate_usd))


"""
This function will return number which will represent price of 1 BTC in CZK

bitcoin_rate = number representing price of 1 BTC in USD

"""
def btc_in_czk(bitcoin_rate):

    r = requests.get('https://api.exchangerate-api.com/v4/latest/USD')
    usd_czk_rate = r.json()['rates']['CZK']
    btc_czk_rate = bitcoin_rate * usd_czk_rate

    return round(btc_czk_rate)


"""
This function will check if {bitcoin_rate} is more or less then {bitcoin_price}

bitcoin_rate = number representing price of 1 BTC in USD
bitcoin_price = number which represent price of bitcoin you would like to check 

"""
def check_bitcoin_rate(bitcoin_rate, bitcoin_price):

    if bitcoin_rate > bitcoin_price:
        return f'Bitcoin is more than {bitcoin_price}, bitcoin is : {bitcoin_rate}'
    else:
        return f'Bitcoin is less than {bitcoin_price}, bitcoin is : {bitcoin_rate}'


while True:
    # Flash notification with btc prices in USD and CZK every two minutes.

    if currency == 1:
        # If user chose CZK

        messages_btc = 'HODL'
        toaster.show_toast(f" btc is {btc_in_czk(get_bitcoin_rate_usd()):,} K CZK", messages_btc, icon_path='.\\icons\\btc.ico', threaded=True, duration=5)
        time.sleep(notification_time)

    if currency == 2:
        # If user chose USD

        messages_btc = 'HODL'
        toaster.show_toast(f" btc is {get_bitcoin_rate_usd():,} K $", messages_btc, icon_path='.\\icons\\btc.ico', threaded=True, duration=5)
        time.sleep(notification_time)

    if currency == 3:
        # If user chose both

        messages_btc = f'btc is {btc_in_czk(get_bitcoin_rate_usd()):,} K CZK'
        toaster.show_toast(f" btc is {get_bitcoin_rate_usd():,} K $", messages_btc, icon_path='.\\icons\\btc.ico', threaded=True, duration=5)
        time.sleep(notification_time)
