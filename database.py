import sqlite3
from pathlib import Path
import os
from colorama import Fore
import pyperclip #copy to clipboard
import password_generator as pg
import encryption
import bcrypt
import menu


BASE_DIR = Path(__file__).parent
DB_NAME = BASE_DIR / 'passwordsDataBase.db'

def create_db():
    with sqlite3.connect(DB_NAME) as connect:
        cursor = connect.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS passwords (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                app_name TEXT NOT NULL,
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
        cursor.execute("SELECT master FROM master_password LIMIT 1")
        result = cursor.fetchone()
        return result is None

def set_master_password(plain_password):
    hashed_password = hash_password(plain_password)
    # Store in database
    with sqlite3.connect(DB_NAME) as connect:
        cursor = connect.cursor()

        cursor.execute("INSERT INTO master_password(master) VALUES (?)", (hashed_password,))

        print("Password stored successfully!")
    input('\nPress Enter to continue...')

def hash_password(plain_password):
    # Convert string to bytes
    password_bytes = plain_password.encode('utf-8')
    
    # Hash the password
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password_bytes, salt)
    return hashed_password

def get_master_password():
    return input(Fore.LIGHTGREEN_EX+'$> ')

def change_master_password(plain_password):
    new_password = hash_password(plain_password)
    with sqlite3.connect(DB_NAME) as connect:
        cursor = connect.cursor()
        cursor.execute("DELETE FROM master_password")
        cursor.execute("INSERT INTO master_password(master) VALUES (?)", (new_password,))
    print("Password changed successfully!")
    input('\nPress Enter to continue...')

def check_master_password(plain_password): # -> bool: 
    password_bytes = plain_password.encode('utf-8')
    with sqlite3.connect(DB_NAME) as connect:
        cursor = connect.cursor()
        cursor.execute("SELECT master FROM master_password LIMIT 1")
        stored_hash = cursor.fetchone()
        return bcrypt.checkpw(password_bytes, stored_hash[0])

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
            cursor.execute("SELECT user_name, password FROM passwords WHERE app_name=?", (app,))
            search_res = cursor.fetchall()
            if search_res:
                print(Fore.LIGHTGREEN_EX+'\n> passwords found: ')
                for id, (user, password) in enumerate(search_res, start=1):
                    print(Fore.LIGHTGREEN_EX+f'{id}. {user}')
                choice = int(input('What password you want to copy? '))
                if 1 <= choice <= len(search_res):
                    user, password = search_res[choice - 1]
                    pyperclip.copy(encryption.decrypt_password(password))
                    print(Fore.LIGHTGREEN_EX+'> Password copied to clipboard.')
                else:
                    print(Fore.GREEN+'\n> Invalid option.')
            else:
                print(Fore.GREEN+'\n> No data found!!')

def add_password():
    with sqlite3.connect(DB_NAME) as connect:
        cursor = connect.cursor()
        app, user, password = get_app()
        encrypted_password = encryption.encrypt_password(password)
        cursor.execute("INSERT INTO passwords(app_name, user_name, password) VALUES (?, ?, ?)", (app, user, encrypted_password))
        print(Fore.GREEN+'\n> Done adding the new password.')
        input('\nPress Enter to continue...')

def delete_password():
    with sqlite3.connect(DB_NAME) as connect:
        cursor = connect.cursor()
        app, user, password = get_app()
        question = input('are you sure you want to delete that password? [y/n]: ')
        if question == 'y':
            row_count_before = cursor.rowcount
            cursor.execute("DELETE FROM passwords WHERE app_name=? AND user_name=?", (app, user))
            if cursor.rowcount < row_count_before:
                print("> Password deleted.")
                input('\nPress Enter to continue...')
            else:
                print("> Password not found.")
                input('\nPress Enter to continue...')
        elif question == 'n':
            pass
        else:
            print(Fore.GREEN+'\n> Enter a valid option!')

def generate_password():
    password = pg.password_gen()
    print(password)
    pyperclip.copy(password)
    print(Fore.LIGHTGREEN_EX+'\n> Password copied to clipboard.')
    input('\nPress Enter to continue...')

def clear():
    os.system("cls" if os.name == "nt" else "clear")

def change_master_password_flow():
    for _ in range(3):
        menu.checking_master_password()
        current_password = get_master_password()

        if not check_master_password(current_password):
            print(Fore.RED + "> Incorrect current password.")
            continue

        while True:
            menu.change_master_password()

            new_password = get_master_password()
            confirm_password = input("Confirm new password: ")

            if new_password != confirm_password:
                print(Fore.RED + "> Passwords do not match. Please try again.")
                continue

            change_master_password(new_password)
            # print(Fore.GREEN + "> Master password changed successfully.")
            break   # or break if this is inside another function

    else:
        print(Fore.RED + "> Too many failed attempts.")
        input('\nPress Enter to continue...')