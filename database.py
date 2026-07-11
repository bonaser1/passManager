import sqlite3
from pathlib import Path
import os
from colorama import Fore
import pyperclip #copy to clipboard
import password_generator as pg
import encryption
import bcrypt


BASE_DIR = Path(__file__).parent
DB_NAME = BASE_DIR / 'passwordsDataBase.db'

def create_db():
    with sqlite3.connect(DB_NAME) as connect:
        cursor = connect.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS passwords (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                website_name TEXT NOT NULL,
                user_name TEXT NOT NULL,
                password TEXT NOT NULL,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        """)
        cursor.execute("CREATE TABLE IF NOT EXISTS master_password (master TEXT NOT NULL, created_at TEXT DEFAULT CURRENT_TIMESTAMP)")

def first_time():
    with sqlite3.connect(DB_NAME) as connect:
        cursor = connect.cursor()

        #checking if the db is empty
        cursor.execute("SELECT 1 FROM master_password LIMIT 1")
        result = cursor.fetchone()
        return True if not result else False

def set_master_password(plain_password):
    """Hashes the password and saves the user to the database."""
    # Convert string to bytes
    password_bytes = plain_password.encode('utf-8')
    
    # Hash the password
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password_bytes, salt)
    
    # Store in database
    with sqlite3.connect(DB_NAME) as connect:
        cursor = connect.cursor()

        cursor.execute("INSERT INTO master_password(master) VALUES (?)", (hashed_password,))

        print("Password stored successfully!")

def get_master_password():
    return input(Fore.LIGHTGREEN_EX+'$> ')

def change_master_password(plain_password):
    new_password = set_master_password(plain_password)
    with sqlite3.connect(DB_NAME) as connect:
        cursor = connect.cursor()

        cursor.execute("UPDATE master_password SET master=?", (new_password,))
    print("Password changed successfully!")

def check_master_password(plain_password): # -> bool: 
    password_bytes = plain_password.encode('utf-8')
    with sqlite3.connect(DB_NAME) as connect:
        cursor = connect.cursor()
        cursor.execute("SELECT 1 FROM master_password LIMIT 1")
        stored_hash = cursor.fetchone()
        for (master,) in stored_hash:
            return bcrypt.checkpw(password_bytes, master)

def get_choice():
    return int(input('$> '))

def get_app_searching():
    app = input('Enter the app name: ')
    return app

def get_app():
    app = input('Enter the app name: ')
    user = input('Enter the username: ')
    password = input('Enter the password: ')
    return app, user, password

def search_passwords():
    with sqlite3.connect(DB_NAME) as connect:
        cursor = connect.cursor()

        #checking if the db is empty
        cursor.execute("SELECT 1 FROM passwords LIMIT 1")
        result = cursor.fetchone()
        if not result:
            print(Fore.GREEN+'\n> No saved passwords')
        else:
            #Searching the db for stored passwords
            app = get_app_searching()
            cursor.execute("SELECT user_name AND password FROM passwords WHERE app_name=?", (app,))
            search_res = cursor.fetchall()
            if search_res:
                print(Fore.LIGHTGREEN_EX+'\n> passwords found: ')
                for id, user, password in enumerate(search_res):
                    print(Fore.LIGHTGREEN_EX+f'{id+1}. {user}')
                    user_password = int(input('What password you want to copy? '))
                    if user_password in range(len(search_res)+1):
                        if user_password == id+1:
                            pyperclip.copy(encryption.decrypt_password(password))
                            print(Fore.LIGHTGREEN_EX+'> Password copied to clipboard.')
                        else:
                            print(Fore.GREEN+'\n> Enter a valid option!')
            else:
                print(Fore.GREEN+'\n> No data found!!')

def add_password():
    with sqlite3.connect(DB_NAME) as connect:
        cursor = connect.cursor()
        app, user, password = get_app()
        encrypted_password = encryption.encrypt_password(password)
        cursor.execute("INSERT INTO passwords(app_name, user_name, password) VALUES (?, ?, ?)", (app, user, encrypted_password))
        print(Fore.GREEN+'\n> Done adding the new password.')

def delete_password():
    with sqlite3.connect(DB_NAME) as connect:
        cursor = connect.cursor()
        app, user, password = get_app()
        encrypted_password = encryption.encrypt_password(password)
        question = input('are you sure you want to delete that password? [y/n]: ')
        if question == 'y':
            cursor.execute("DELETE FROM passwords WHERE app_name=? AND user_name=? AND password=?", (app, user, encrypted_password))
            print(Fore.GREEN+'\n> the password has been deleted.')
        elif question == 'n':
            pass
        else:
            print(Fore.GREEN+'\n> Enter a valid option!')

def generate_password():
    password = pg.password_gen()
    print(password)
    pyperclip.copy(password)
    print(Fore.LIGHTGREEN_EX+'> Password copied to clipboard.')

def clear():
    os.system("cls" if os.name == "nt" else "clear")