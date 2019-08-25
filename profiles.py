import sqlite3

conn = sqlite3.connect('profiles.db')
c = conn.cursor()

# Create Table in DB
c.execute("""CREATE TABLE users(
             name text,
             bitcoin integer,
             currency integer    )""")


# Create profile with your information
def create_profile(name, bitcoins, currency):
    with conn:
        c.execute(f"INSERT INTO users VALUES ('{name}', '{bitcoins}', '{currency}')")


# Update profile which already exist in DB
def update_profile(name, bitcoins):
    with conn:
        c.execute(f"UPDATE users SET bitcoin = {bitcoins}")


# Delete profile which already exist in DB
def delete_profile(name):
    with conn:
        c.execute(f"DELETE from users WHERE name LIKE '%{name}%' ")
