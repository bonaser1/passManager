import os
import sqlite3
from pathlib import Path
import pyperclip
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

def clear() -> None:
    os.system("cls" if os.name == "nt" else "clear")

def pause():
    input("\nPress Enter to continue...")
    clear()

def success(message):
    print(f"\033[32m{message}\033[0m")
    pause()

def error(message):
    print(f"\033[31m{message}\033[0m")
    pause()


# ------------------------
# Main function
# ------------------------

def main_func() -> None:
    while True:
        menu.verifying_master_password()
        plain_password = get_master_password()
        if verify_master_password(plain_password):
            clear()
            break
        error("> Incorrect master password. Please try again.")
        
    while True:

        menu.main()
        try:
            choice = get_choice()

        except ValueError:
            error("> Please enter a number.")
            continue
        
        if choice == 1:
            search_passwords()

        elif choice == 2:
            add_password()

        elif choice == 3:
            if not if_passwords_exists():
                error("\n> No saved passwords")
            else:
                domain, user, password = get_info()
                delete_password(domain, user)

        elif choice == 4:
            generate_password()

        elif choice == 5:
            change_master_password_flow()
                    
        elif choice == 0:
            break

        else:
            error("\n> Enter a valid option.")


# ------------------------
# Get input
# ------------------------

def get_choice() -> int:
    return int(input('> Choose an option: '))

def search_by_domain() -> str:
    domain = input('\n> Enter the domain name: ')
    return domain

def get_info() -> tuple[str, str, str]:
    domain = input('\n> Enter the domain name: ')
    user = input('> Enter the username: ')
    password = input('> Enter the password: ')
    return domain, user, password

# ------------------------
# DataBase
# ------------------------

def create_db() -> None:
    with sqlite3.connect(DB_NAME) as connect:
        cursor = connect.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS passwords (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                domain_name TEXT NOT NULL,
                user_name TEXT NOT NULL,
                password TEXT NOT NULL,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        """)
        cursor.execute("CREATE TABLE IF NOT EXISTS master_password (master TEXT NOT NULL, created_at TEXT DEFAULT CURRENT_TIMESTAMP)")

def hash_password(plain_password) -> str:
    password_bytes = plain_password.encode('utf-8')
    
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password_bytes, salt)
    return hashed_password


# ------------------------
# Master Password
# ------------------------

def check_master_password() -> bool:
    with sqlite3.connect(DB_NAME) as connect:
        cursor = connect.cursor()

        cursor.execute("SELECT master FROM master_password LIMIT 1")
        result = cursor.fetchone()
        return result is None
    
def set_master_password(plain_password) -> None:
    hashed_password = hash_password(plain_password)
    with sqlite3.connect(DB_NAME) as connect:
        cursor = connect.cursor()

        cursor.execute("INSERT INTO master_password(master) VALUES (?)", (hashed_password,))

        success("> Password stored successfully.")

def get_master_password() -> str:
    return input('> Enter master password: ')

def verify_master_password(plain_password) -> bool: 
    password_bytes = plain_password.encode('utf-8')
    with sqlite3.connect(DB_NAME) as connect:
        cursor = connect.cursor()
        cursor.execute("SELECT master FROM master_password LIMIT 1")
        stored_hash = cursor.fetchone()
        return bcrypt.checkpw(password_bytes, stored_hash[0])

def change_master_password(plain_password) -> None:
    new_password = hash_password(plain_password)
    with sqlite3.connect(DB_NAME) as connect:
        cursor = connect.cursor()
        cursor.execute("DELETE FROM master_password")
        cursor.execute("INSERT INTO master_password(master) VALUES (?)", (new_password,))
    success("> Password changed successfully.")

def change_master_password_flow() -> None:
    for _ in range(3):
        menu.verifing_master_password()
        current_password = get_master_password()

        if not verify_master_password(current_password):
            error("> Incorrect current password.")
            continue

        while True:
            menu.change_master_password()

            new_password = get_master_password()
            confirm_password = input("> Confirm new password: ")

            if new_password != confirm_password:
                error("> Passwords do not match. Please try again.")
                continue

            change_master_password(new_password)
            break
        break

    else:
        error("> Too many failed attempts.")


# ------------------------
# Managing passwords
# ------------------------

def if_passwords_exists() -> bool:
    with sqlite3.connect(DB_NAME) as connect:
        cursor = connect.cursor()

        cursor.execute("SELECT 1 FROM passwords LIMIT 1")
        result = cursor.fetchone()
        if not result:
            return False
        return True

def search_passwords() -> None:
    if not if_passwords_exists():
        error("\n> No saved passwords")
    else:
        with sqlite3.connect(DB_NAME) as connect:
            cursor = connect.cursor()
            domain = search_by_domain()
            cursor.execute("SELECT user_name, password FROM passwords WHERE domain_name=?", (domain,))
            search_res = cursor.fetchall()
            if search_res:
                print('\n> passwords found: ')
                for id, (user, password) in enumerate(search_res, start=1):
                    print(f'    {id}. {user}')
                choice = int(input('\n> Choose a user: '))
                if 1 <= choice <= len(search_res):
                    user, password = search_res[choice - 1]
                    
                else:
                    error("\n> Invalid option.")
                menu.options_list()
                option = input('> Choose an option: ')
                if option.upper() == 'C':
                    pyperclip.copy(decrypt_password(password))
                    success("> Password copied to clipboard.")
                elif option.upper() == 'V':
                    print(decrypt_password(password))
                    pause()
                elif option.upper() == 'D':
                    delete_password(domain, user)
                elif option.upper() == 'E':
                    domain, user, password = get_info()
                    edit_password(domain, user)
                else:
                    error("\n> Invalid option.")
            else:
                error("\n> No data found.")

def add_password() -> None:
    with sqlite3.connect(DB_NAME) as connect:
        cursor = connect.cursor()
        domain, user, password = get_info()
        encrypted_password = encrypt_password(password)
        cursor.execute("INSERT INTO passwords(domain_name, user_name, password) VALUES (?, ?, ?)", (domain, user, encrypted_password))
        success("\n> Done adding the new password.")

def edit_password(domain, user) -> None:
    while True:
        new_password = input('> Enter the new password: ')
        confirm_new_password = input('> Confirm the new password: ')
        if new_password == confirm_new_password:
            encrypted_password = encrypt_password(new_password)
            with sqlite3.connect(DB_NAME) as connect:
                cursor = connect.cursor()
                cursor.execute("UPDATE passwords SET password=? WHERE domain_name=? AND user_name=? ", (encrypted_password, domain, user))
                success("> Password modified successfully.")
                break
        else:
            error("> Passwords do not match. Please try again.")
            continue

def delete_password(domain, user) -> None:
    if not if_passwords_exists():
        error("\n> No saved passwords")
    else:
        with sqlite3.connect(DB_NAME) as connect:
            cursor = connect.cursor()
            question = input('> are you sure you want to delete that password? [y/n]: ')
            if question == 'y':
                cursor.execute("DELETE FROM passwords WHERE domain_name=? AND user_name=?", (domain, user))
                if cursor.rowcount == 0:
                    error("> Password not found.")
                else:
                    success("> Password deleted.")
                    
            elif question == 'n':
                pass
            else:
                error("\n> Enter a valid option.")

def generate_password(length=20) -> None:
    chars = string.ascii_letters+string.digits+string.punctuation
    password = ''.join(secrets.choice(chars) for _ in range(length))
    print(password)
    pyperclip.copy(password)
    success("\n> Password copied to clipboard.")

# ------------------------
# Encryption
# ------------------------

def generate_and_save_key() -> None: 
    if KEY_FILE.exists():
        return
    key = Fernet.generate_key()
    with open("secret.key", "wb") as key_file:
        key_file.write(key)
    print("Encryption key generated and saved as 'secret.key'.")

def load_key() -> None:
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