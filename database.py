import sqlite3
from pathlib import Path
import os
from colorama import Fore
import pyperclip #copy to clipboard
import password_generator as pg


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

def get_app_searching():
    app = input('Enter the app name: ')
    return app

def get_app():
    app = input('Enter the app name: ')
    user = input('Enter the username: ')
    password = input('Enter the password: ')
    return app, user, password

def get_choice():
    return int(input('$> '))

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
                            pyperclip.copy(pg.decrypt_password(password))
                            print(Fore.LIGHTGREEN_EX+'> Password copied to clipboard.')
                        else:
                            print(Fore.GREEN+'\n> Enter a valid option!')
            else:
                print(Fore.GREEN+'\n> No data found!!')

def add_password():
    with sqlite3.connect(DB_NAME) as connect:
        cursor = connect.cursor()
        app, user, password = get_app()
        encrypted_password = pg.encrypt_password(password)
        cursor.execute("INSERT INTO passwords(app_name, user_name, password) VALUES (?, ?, ?)", (app, user, encrypted_password))
        print(Fore.GREEN+'\n> Done adding the new password.')

def delete_password():
    with sqlite3.connect(DB_NAME) as connect:
        cursor = connect.cursor()
        app, user, password = get_app()
        encrypted_password = pg.encrypt_password(password)
        question = input('are you sure you want to delete that password? [y/n]: ')
        if question == 'y':
            cursor.execute("DELETE FROM passwords WHERE app_name=? AND user_name=? AND password=?", (app, user, encrypted_password))
            print(Fore.GREEN+'\n> the password has been deleted.')
        elif question == 'n':
            pass
        else:
            print(Fore.GREEN+'\n> Enter a valid option!')

def clear():
    os.system("cls" if os.name == "nt" else "clear")