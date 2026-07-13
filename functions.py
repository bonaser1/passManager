import encryption
import os
import sqlite3
from pathlib import Path
import functions
import pyperclip
import encryption
import bcrypt
import menu
import secrets
import string
from cryptography.fernet import Fernet

# ------------------------
# Variables
# ------------------------

BASE_DIR = Path(__file__).parent
DB_NAME = BASE_DIR/'passwordsDataBase.db'
KEY_FILE = Path("secret.key")

# ------------------------
# OS
# ------------------------

def clear():
    os.system("cls" if os.name == "nt" else "clear")


# ------------------------
# Main function
# ------------------------

def main_func():
    while True:
        menu.verifing_master_password()
        plain_password = get_master_password()
        if verify_master_password(plain_password):
            clear()
            break
        print(f"\033[31m{"> Incorrect master password. Please try again."}\033[0m")
        
    while True:

        menu.main()
        try:
            interface3_choice = get_choice()

        except ValueError:
            print(f"\033[31m{"> Please enter a number."}\033[0m")
            input('\nPress Enter to continue...')
            clear()
            continue
        
        if interface3_choice == 1:
            search_passwords()

        elif interface3_choice == 2:
            add_password()

        elif interface3_choice == 3:
            app, user, password = get_app()
            delete_password(app, user)

        elif interface3_choice == 4:
            generate_password()

        elif interface3_choice == 5:
            change_master_password_flow()
                    
        elif interface3_choice == 0:
            break

        else:
            print(f"\033[31m{"\n> Enter a valid option."}\033[0m") 
            input('\nPress Enter to continue...')
            clear()


# ------------------------
# Get input
# ------------------------

def get_choice():
    return int(input('> Choose an option: '))

def searche_by_app():
    app = input('\n> Enter the app name: ')
    return app

def get_app():
    app = input('\n> Enter the app name: ')
    user = input('> Enter the username: ')
    password = input('> Enter the password: ')
    return app, user, password

# ------------------------
# DataBase
# ------------------------

def connect_database(path):
    sqlite3.connect(path)

def create_db():
    with connect_database(DB_NAME) as connect:
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

def hash_password(plain_password):
    password_bytes = plain_password.encode('utf-8')
    
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password_bytes, salt)
    return hashed_password


# ------------------------
# Master Password
# ------------------------

def check_master_password():
    with connect_database(DB_NAME) as connect:
        cursor = connect.cursor()

        cursor.execute("SELECT master FROM master_password LIMIT 1")
        result = cursor.fetchone()
        return result is None
    
def set_master_password(plain_password):
    hashed_password = hash_password(plain_password)
    with connect_database(DB_NAME) as connect:
        cursor = connect.cursor()

        cursor.execute("INSERT INTO master_password(master) VALUES (?)", (hashed_password,))

        print(f"\033[32m{"> Password stored successfully."}\033[0m")
    input('\nPress Enter to continue...')
    clear()

def get_master_password():
    return input('> Enter master password: ')

def verify_master_password(plain_password) -> bool: 
    password_bytes = plain_password.encode('utf-8')
    with connect_database(DB_NAME) as connect:
        cursor = connect.cursor()
        cursor.execute("SELECT master FROM master_password LIMIT 1")
        stored_hash = cursor.fetchone()
        return bcrypt.checkpw(password_bytes, stored_hash[0])

def change_master_password(plain_password):
    new_password = hash_password(plain_password)
    with connect_database(DB_NAME) as connect:
        cursor = connect.cursor()
        cursor.execute("DELETE FROM master_password")
        cursor.execute("INSERT INTO master_password(master) VALUES (?)", (new_password,))
    print(f"\033[32m{"> Password changed successfully."}\033[0m")
    input('\nPress Enter to continue...')
    clear()

def change_master_password_flow():
    for _ in range(3):
        menu.verifing_master_password()
        current_password = get_master_password()

        if not check_master_password(current_password):
            print(f"\033[31m{"> Incorrect current password."}\033[0m")
            continue

        while True:
            menu.change_master_password()

            new_password = get_master_password()
            confirm_password = input("> Confirm new password: ")

            if new_password != confirm_password:
                print(f"\033[31m{"> Passwords do not match. Please try again."}\033[0m") #
                continue

            change_master_password(new_password)
            break
        break

    else:
        print(f"\033[31m{"> Too many failed attempts."}\033[0m")
        input('\nPress Enter to continue...')
        clear()


# ------------------------
# Managing passwords
# ------------------------

def search_passwords():
    with connect_database(DB_NAME) as connect:
        cursor = connect.cursor()

        cursor.execute("SELECT 1 FROM passwords LIMIT 1")
        result = cursor.fetchone()
        if not result:
            print(f"\033[31m{"\n> No saved passwords"}\033[0m")
            input('\nPress Enter to continue...')
            clear()
        else:
            app = searche_by_app()
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
                    pyperclip.copy(decrypt_password(password))
                    print(f"\033[32m{"> Password copied to clipboard."}\033[0m")
                    input('\nPress Enter to continue...')
                    clear()
                elif option.upper() == 'V':
                    print(decrypt_password(password))
                    input('\nPress Enter to continue...')
                    clear()
                elif option.upper() == 'D':
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
    with connect(DB_NAME) as connect:
        cursor = connect.cursor()
        app, user, password = get_app()
        encrypted_password = encryption.encrypt_password(password)
        cursor.execute("INSERT INTO passwords(app_name, user_name, password) VALUES (?, ?, ?)", (app, user, encrypted_password))
        print(f"\033[32m{"\n> Done adding the new password."}\033[0m")
        input('\nPress Enter to continue...')
        clear()

def edit_password(app, user):
    while True:
        new_password = input('> Enter the new password: ')
        confirm_new_password = input('> Confirm the new password: ')
        if new_password == confirm_new_password:
            hashed_new_password = hash_password(new_password)
            with connect_database(DB_NAME) as connect:
                cursor = connect.cursor()
                cursor.execute("UPDATE passwords SET password=? WHERE app_name=? AND user_name=? ", (hashed_new_password, app, user))
                print(f"\033[32m{"> Password modified successfully."}\033[0m")
                input('\nPress Enter to continue...')
                clear()
                break
        else:
            print(f"\033[31m{"> Passwords do not match. Please try again."}\033[0m")
            continue

def delete_password(app, user):
    with connect_database(DB_NAME) as connect:
        cursor = connect.cursor()
        
        question = input('> are you sure you want to delete that password? [y/n]: ')
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

def generate_password(length=20):
    chars = string.ascii_letters+string.digits+string.punctuation
    password = ''.join(secrets.choice(chars) for _ in range(length))
    print(password)
    pyperclip.copy(password)
    print(f"\033[32m{"\n> Password copied to clipboard."}\033[0m")
    input('\nPress Enter to continue...')
    clear()

# ------------------------
# Encryption
# ------------------------

def generate_and_save_key(): 
    if KEY_FILE.exists():
        return
    key = Fernet.generate_key()
    with open("secret.key", "wb") as key_file:
        key_file.write(key)
    print("Encryption key generated and saved as 'secret.key'.")

def load_key():
    return open("secret.key", "rb").read()

def encrypt_password(password: str) -> str:
    key = load_key()
    f = Fernet(key)
    encrypted_bytes = f.encrypt(password.encode())
    return encrypted_bytes.decode()

def decrypt_password(encrypted_password: str) -> str:
    key = load_key()
    f = Fernet(key)
    decrypted_bytes = f.decrypt(encrypted_password.encode())
    return decrypted_bytes.decode()