import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).parent
DB_NAME = BASE_DIR / 'passwordsDataBase.db'



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
            print('\n>>> No saved passwords')
        else:
            #Searching the db for stored passwords
            app = get_app_searching()
            cursor.execute("SELECT password FROM passwords WHERE app_name=? AND user_name=?", (app,))
            search_res = cursor.fetchall()
            if search_res:
                print('passwords found: ')
                for password in search_res:
                    print(f'>>> {password}')
            else:
                print('\n>>> No data found!!')

def add_password():
    with sqlite3.connect(DB_NAME) as connect:
        cursor = connect.cursor()
        app, user, password = get_app()
        cursor.execute("INSERT INTO passwords(app_name, user_name, password) VALUES (?, ?, ?)", (app, user, password))
        print(f'\n>>> Done adding the new password.')

def delete_password():
    with sqlite3.connect(DB_NAME) as connect:
        cursor = connect.cursor()
        app, user, password = get_app()
        question = input('are you sure you want to delete that password? [y/n]: ')
        if question == 'y':
            cursor.execute("DELETE FROM passwords WHERE app_name=? AND user_name=? AND password=?", (app, user, password))
            print(f'\n>>> the password has been deleted.')
        elif question == 'n':
            pass
        else:
            print('\n>>> Enter a valid value!!')
