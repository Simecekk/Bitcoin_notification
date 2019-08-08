import requests
import time
from win10toast import ToastNotifier

toaster = ToastNotifier()


def get_bitcoin_rate_usd():

    r = requests.get('https://api.coindesk.com/v1/bpi/currentprice.json')
    bitcoin_rate_usd = r.json()['bpi']['USD']['rate'].replace(',', '')
    return round(float(bitcoin_rate_usd))


def btc_in_czk(bitcoin_rate):

    r = requests.get('https://api.exchangerate-api.com/v4/latest/USD')
    usd_czk_rate = r.json()['rates']['CZK']
    btc_czk_rate = bitcoin_rate * usd_czk_rate

    return round(btc_czk_rate)


def check_bitcoin_rate(bitcoin_rate, bitcoin_price):

    if bitcoin_rate > bitcoin_price:
        return f'Bitcoin is more than {bitcoin_price}, bitcoin is : {bitcoin_rate}'
    else:
        return f'Bitcoin is less than {bitcoin_price}, bitcoin is : {bitcoin_rate}'


while True:

    messages_btc = f'btc is {btc_in_czk(get_bitcoin_rate_usd()):,} K CZK'
    toaster.show_toast(f" btc is {get_bitcoin_rate_usd():,} K $", messages_btc, icon_path='.\\icons\\btc.ico', threaded=True, duration=5)
    time.sleep(120)
