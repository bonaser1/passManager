import sqlite3
from pathlib import Path
import os
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

        print(f"\033[32m{"Password stored successfully."}\033[0m")
    input('\nPress Enter to continue...')
    clear()

def hash_password(plain_password):
    # Convert string to bytes
    password_bytes = plain_password.encode('utf-8')
    
    # Hash the password
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password_bytes, salt)
    return hashed_password

def get_master_password():
    return input('$> ')

def change_master_password(plain_password):
    new_password = hash_password(plain_password)
    with sqlite3.connect(DB_NAME) as connect:
        cursor = connect.cursor()
        cursor.execute("DELETE FROM master_password")
        cursor.execute("INSERT INTO master_password(master) VALUES (?)", (new_password,))
    print(f"\033[32m{"Password changed successfully."}\033[0m")
    input('\nPress Enter to continue...')
    clear()

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
    app = input('\nEnter the app name: ')
    return app

def get_app():
    app = input('\nEnter the app name: ')
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
            print(f"\033[31m{"\n> No saved passwords"}\033[0m")
            input('\nPress Enter to continue...')
            clear()
        else:
            #Searching the db for stored passwords
            app = get_app_searching()
            cursor.execute("SELECT user_name, password FROM passwords WHERE app_name=?", (app,))
            search_res = cursor.fetchall()
            if search_res:
                print('\n> passwords found: ')
                for id, (user, password) in enumerate(search_res, start=1):
                    print(f'    {id}. {user}')
                choice = int(input('\n> Choose a user: '))
                if 1 <= choice <= len(search_res):
                    user, password = search_res[choice - 1]
                    
                else:
                    print(f"\033[31m{"\n> Invalid option."}\033[0m")
                    input('\nPress Enter to continue...')
                    clear()
                menu.options_list()
                option = input('\n> Choose an option: ')
                if option.upper() == 'C':
                    pyperclip.copy(encryption.decrypt_password(password))
                    print(f"\033[32m{"> Password copied to clipboard."}\033[0m")
                    input('\nPress Enter to continue...')
                    clear()
                elif option.upper() == 'V':
                    print(encryption.decrypt_password(password))
                    input('\nPress Enter to continue...')
                    clear()
                elif option.upper() == 'D':
                    # app, user, password = get_app()
                    delete_password(app, user)
                    input('\nPress Enter to continue...')
                    clear()
                elif option.upper() == 'E':
                    app, user, password = get_app()
                    edit_password(app, user)
                else:
                    print(f"\033[31m{"\n> Invalid option."}\033[0m")
                    input('\nPress Enter to continue...')
                    clear()
            else:
                print(f"\033[31m{"\n> No data found."}\033[0m")
                input('\nPress Enter to continue...')
                clear()

def add_password():
    with sqlite3.connect(DB_NAME) as connect:
        cursor = connect.cursor()
        app, user, password = get_app()
        encrypted_password = encryption.encrypt_password(password)
        cursor.execute("INSERT INTO passwords(app_name, user_name, password) VALUES (?, ?, ?)", (app, user, encrypted_password))
        print(f"\033[32m{"\n> Done adding the new password."}\033[0m")
        input('\nPress Enter to continue...')
        clear()

def delete_password(app, user):
    with sqlite3.connect(DB_NAME) as connect:
        cursor = connect.cursor()
        
        question = input('are you sure you want to delete that password? [y/n]: ')
        if question == 'y':
            row_count_before = cursor.rowcount()
            cursor.execute("DELETE FROM passwords WHERE app_name=? AND user_name=?", (app, user))
            if cursor.rowcount() < row_count_before:
                print(f"\033[32m{"> Password deleted."}\033[0m")
                input('\nPress Enter to continue...')
                clear()
            else:
                print(f"\033[31m{"> Password not found."}\033[0m")
                input('\nPress Enter to continue...')
                clear()
        elif question == 'n':
            pass
        else:
            print(f"\033[31m{"\n> Enter a valid option!"}\033[0m")

def edit_password(app, user):
    while True:
        new_password = input('Enter the new password: ')
        confirm_new_password = input('Confirm the new password: ')
        if new_password == confirm_new_password:
            hashed_new_password = hash_password(new_password)
            with sqlite3.connect(DB_NAME) as connect:
                cursor = connect.cursor()
                # cursor.execute("DELETE FROM passwords WHERE app_name=? AND user_name=?", (app, user))
                cursor.execute("UPDATE passwords SET password=? WHERE app_name=? AND user_name=? ", (hashed_new_password, app, user))
                print(f"\033[32m{"Password modified successfully."}\033[0m")
                input('\nPress Enter to continue...')
                clear()
                break
        else:
            print(f"\033[31m{"> Passwords do not match. Please try again."}\033[0m")
            continue


def generate_password():
    password = pg.password_gen()
    print(password)
    pyperclip.copy(password)
    print(f"\033[32m{"\n> Password copied to clipboard."}\033[0m")
    input('\nPress Enter to continue...')
    clear()

def clear():
    os.system("cls" if os.name == "nt" else "clear")

def change_master_password_flow():
    for _ in range(3):
        menu.checking_master_password()
        current_password = get_master_password()

        if not check_master_password(current_password):
            print(f"\033[31m{"> Incorrect current password."}\033[0m")
            continue

        while True:
            menu.change_master_password()

            new_password = get_master_password()
            confirm_password = input("Confirm new password: ")

            if new_password != confirm_password:
                print(f"\033[31m{"> Passwords do not match. Please try again."}\033[0m") #
                continue

            change_master_password(new_password)
            # print(Fore.GREEN + "> Master password changed successfully.")
            break   # or break if this is inside another function
        break

    else:
        print(f"\033[31m{"> Too many failed attempts."}\033[0m")
        input('\nPress Enter to continue...')
        clear()