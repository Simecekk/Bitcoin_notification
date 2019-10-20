import requests
import time
from win10toast import ToastNotifier
from menu import menu, profile

toaster = ToastNotifier()


print(' Welcome in Balarm. Bitcoin notification app for windows')
print('*********************************************************')

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


 # returns worth of yours bitcoin in CZK
def czk_bitcoin_worth(price_in_czk): 
     worth_in_czk = price_in_czk * profile[0][1]
     return round(worth_in_czk)


if __name__ == '__main__':
    
    menu()

    def czk_bitcoin_worth(price_in_czk): 
        worth_in_czk = price_in_czk * profile[0][1]
        return round(worth_in_czk)

    while True:
        # Flash notification with btc prices in USD and CZK every two minutes.

        if profile[0][2] == 1:
            # If user chose CZK

            messages_btc = 'HODL'
            toaster.show_toast(f" btc is {btc_in_czk(get_bitcoin_rate_usd()):,} K CZK", messages_btc, icon_path='.\\icons\\btc.ico', threaded=True, duration=5)
            time.sleep(120)

        if profile[0][2] == 2:
            # If user chose USD

            messages_btc = 'HODL'
            toaster.show_toast(f" btc is {get_bitcoin_rate_usd():,} K $", messages_btc, icon_path='.\\icons\\btc.ico', threaded=True, duration=5)
            time.sleep(120)

        if profile[0][2] == 3:
            # If user chose both

            messages_btc = f'btc is {btc_in_czk(get_bitcoin_rate_usd()):,} K CZK\nYou own {czk_bitcoin_worth(btc_in_czk(get_bitcoin_rate_usd())):,} CZK '
            toaster.show_toast(f" btc is {get_bitcoin_rate_usd():,} K $", messages_btc, icon_path='.\\icons\\btc.ico', threaded=True, duration=7)
            time.sleep(120)
