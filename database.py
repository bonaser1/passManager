import sqlite3

DB_NAME = 'passwordsDataBase.db'

with sqlite3.connect(DB_NAME) as connect:
    cursor = connect.cursor()

    def get_app_searching():
        app = input('Enter the app name: ')
        user = input('Enter the username: ')
        return app, user

    def get_app():
        app = input('Enter the app name: ')
        user = input('Enter the username: ')
        password = input('Enter the password: ')
        return app, user, password

    def get_choice():
        return int(input('$> '))

    def search_passwords(cursor):
        #checking if the db is empty
        cursor.execute("SELECT 1 FROM passwords LIMIT 1")
        result = cursor.fetchone()
        if result is None:
            print('No saved passwords')
        else:
            #Searching the db for stored passwords
            app, user = get_app_searching()
            cursor.execute("SELECT password FROM passwords WHERE app_name=? AND user_name=?", (app, user))
            search_res = cursor.fetchone()
            if search_res:
                print('passwords found: ')
                print(f'    {search_res[0]}')
            else:
                print('No data found!!')

    def add_password(cursor):
        app, user, password = get_app()
        cursor.execute("INSERT INTO passwords(app_name, user_name, password) VALUES (?, ?, ?)", (app, user, password))
        print(f'Done adding the new password.')

    def delete_password(cursor):
        app, user, password = get_app()
        question = input('are you sure you want to delete that password? [y/n]: ')
        if question == 'y':
            cursor.execute("DELETE FROM passwords WHERE app_name=? AND user_name=? AND password=?", (app, user, password))
            print(f'the password has been deleted.')
        elif question == 'n':
            pass
        else:
            print('Enter a valid value!!')

    def generating_password():
        pass