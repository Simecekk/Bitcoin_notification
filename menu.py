from profiles import create_profile, delete_profile, update_profile, c


# profile = profile which user chose to use.
profile = []


def menu():

    print("")
    print("1) Create profile \n2) Delete profile \n3) Update profile \n4) Show me my profiles \n5) Get notifications")
    print('\n')

    choice = input('Your choice? : ')

    # Add profile to DB
    if choice == '1':
        name = str(input('Choose name of the profile: '))
        bitcoins = float(input('How much bitcoins you have?: '))
        print('Which currency do you want to use?')
        currency = int(input('1 = CZK \n2 = USD \n3 = both \ntype here: '))
        create_profile(name, bitcoins, currency)
        print('*********************************************************')
        menu()

    # Delete profile from DB
    elif choice == '2':
        c.execute("SELECT * FROM users")
        try:
            print(c.fetchall())
        except:
            print('Nothing here')
            print('\n')
            menu()
        deleted_name = str(input('Type name of profile, which you want to delete: '))
        delete_profile(deleted_name)
        print('*********************************************************')
        menu()

    # Update bitcoins you have.
    elif choice == '3':
        print('Which profile you want to update?')
        c.execute("SELECT * FROM users")
        print(c.fetchall()[0])
        updated_profile = str(input('Type name of your profile: '))
        updated_profile_bitcoins = float(input('Update your bitcoins: '))
        update_profile(updated_profile, updated_profile_bitcoins)
        print('*********************************************************')
        menu()

    # Display all profiles
    elif choice == '4':

        c.execute("SELECT * FROM users")
        print('There are those profiles')
        print(c.fetchall())
        print('*********************************************************')
        menu()

    elif choice == '5':
        c.execute("SELECT * FROM users")
        try:
            print(c.fetchall())
        except:
            print('You have to create profile first.')
            print('\n')
            menu()

        used_profile = str(input('Type name of profile you want to use: '))
        c.execute(f"SELECT * FROM users WHERE name LIKE '%{used_profile}%' ")
        profile.append(c.fetchone())
        return profile

    else:
        print('Wrong choice, try again.')
        print('*********************************************************')
        menu()
