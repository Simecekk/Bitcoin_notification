import sqlite3
import time
from functools import partial
from tkinter import *

from win10toast import ToastNotifier

from balarm import (btc_in_czk, check_bitcoin_rate, czk_bitcoin_worth,
                    get_bitcoin_rate_usd)

conn = sqlite3.connect('profiles.db')
c = conn.cursor()

toaster = ToastNotifier()

class Notificator():

    def __init__(self, master):


        # Profile frame

        profile_frame = Frame(master)
        profile_frame.grid(row=0, column=0)

        c.execute("SELECT * FROM users")
        i = 1
        for profile in c.fetchall():
            profile_label = Label(profile_frame, text=f'{profile[0]} {profile[1]} btc')
            profile_label.grid(row=i, column=0)
            i += 1

        profile_label = Label(profile_frame, text='Your profiles', bg='grey')
        profile_label.grid(row=0, column=0)

        # Create frame
        name = StringVar()
        bitcoins = DoubleVar()
        currency = IntVar()

        create_frame = Frame(master)
        create_frame.grid(row=0, column=1)

        create_label = Label(create_frame, text='Create your profiles', bg='grey')
        create_label.grid(row=0, column=0)

        create_label_name = Label(create_frame, text='Name')
        create_label_name.grid(row=1, column=0)
        profile_name = Entry(create_frame, textvariable=name)
        profile_name.grid(row=1, column=1)

        create_label_btc = Label(create_frame, text='btc')
        create_label_btc.grid(row=2, column=0)
        profile_btc = Entry(create_frame, textvariable=bitcoins)
        profile_btc.grid(row=2, column=1)

        create_label_currency = Label(create_frame, text='1-USD 2-CZK 3-BOTH')
        create_label_currency.grid(row=3, column=0)
        profile_currency = Entry(create_frame, textvariable=currency)
        profile_currency.grid(row=3, column=1)

        create_button = Button(create_frame, text='create', command=partial(self.create_profile, name, bitcoins, currency))
        create_button.grid(row=4, column=1)

        # Run frame
        name = StringVar()

        run_frame = Frame(master)
        run_frame.grid(row=1, column=0)

        run_label = Label(run_frame, text='Start notificator', bg='grey')
        run_label.grid(row=0, column=0)

        run_label_name = Label(run_frame, text='Type name of profile you want to use')
        run_label_name.grid(row=1, column=0)
        profile_name = Entry(run_frame, textvariable=name)
        profile_name.grid(row=2, column=0)

        run_button = Button(run_frame, text='run', command=partial(self.run, name))
        run_button.grid(row=3, column=0)

        # Delete frame
        name = StringVar()

        delete_frame = Frame(master)
        delete_frame.grid(row=1, column=1)

        delete_label = Label(delete_frame, text='delete your profiles', bg='grey')
        delete_label.grid(row=0, column=0)

        delete_label_name = Label(delete_frame, text='Name')
        delete_label_name.grid(row=1, column=0)
        profile_name = Entry(delete_frame, textvariable=name)
        profile_name.grid(row=1, column=1)

        delete_button = Button(delete_frame, text='delete', command=partial(self.delete_profile, name))
        delete_button.grid(row=2, column=1)

        # Update frame
        name = StringVar()
        bitcoins = DoubleVar()
        
        update_frame = Frame(master)
        update_frame.grid(row=2, column=1)

        update_label = Label(update_frame, text='update your profiles', bg='grey')
        update_label.grid(row=0, column=0)

        update_label_name = Label(update_frame, text='Name')
        update_label_name.grid(row=1, column=0)
        profile_name = Entry(update_frame,  textvariable=name)
        profile_name.grid(row=1, column=1)

        update_label_btc = Label(update_frame, text='btc')
        update_label_btc.grid(row=2, column=0)
        profile_btc = Entry(update_frame, textvariable=bitcoins)
        profile_btc.grid(row=2, column=1)

        update_button = Button(update_frame, text='update', command=partial(self.update_profile, name, bitcoins))
        update_button.grid(row=3, column=1)


    def create_profile(self, name, bitcoins, currency):
        with conn:
            c.execute(f"INSERT INTO users VALUES ('{str(name.get())}', '{float(bitcoins.get())}', '{int(currency.get())}')")

    def delete_profile(self, name):
        with conn:
            c.execute(f"DELETE from users WHERE name LIKE '%{str(name.get())}%' ")

    def update_profile(self, name, bitcoins):
        with conn:
            c.execute(f"UPDATE users SET bitcoin = {float(bitcoins.get())} WHERE name LIKE '%{str(name.get())}%'")

    def run(self, name):
        
        profile = []

        c.execute(f"SELECT * FROM users WHERE name LIKE '%{str(name.get())}%' ")
        profile.append(c.fetchone())

        def czk_bitcoin_worth(price_in_czk): 
            worth_in_czk = price_in_czk * profile[0][1]
            return round(worth_in_czk)

        while True:

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


root = Tk()
balarm_gui = Notificator(root)
root.mainloop()
