import sqlite3, menu

def get_app_searching():
    app = input('Enter the app name: ')
    user = input('Enter the username: ')
    return app, user

def get_app():
    app = input('Enter the app name: ')
    user = input('Enter the username: ')
    password = input('Enter the password: ')
    return app, user, password

def search_passwords():
    #checking if the db is empty
    cursor.execute("SELECT 1 FROM passwords LIMIT 1")
    result = cursor.fetchone()
    if result is None:
        print('No saved passwords')
    else:
        #Searching the db for stored passwords
        app, user = get_app_searching()
        cursor.execute("SELECT password FROM passwords WHERE app_name=? AND user_name=?", (app, user))
        search_res = cursor.fetchall()
        if search_res:
            print('passwords found: ')
            print(f'    {search_res}')
        else:
            print('No data found!!')

def add_password():
    app, user, password = get_app()
    cursor.execute("INSERT INTO passwords(app_name, user_name, password) VALUES (?, ?, ?)", (app, user, password))
    print(f'Done adding the new password.')

def delete_password():
    app, user, password = get_app()
    qustion = input('are you sure you want to delete that password? [y/n]: ')
    if qustion == 'y':
        cursor.execute("DELETE FROM passwords WHERE app_name=? AND user_name=? AND password=?", (app, user, password))
        print(f'the password has been deleted.')
        # connect.commit()
        #return to main menu
    elif qustion == 'n':
        pass
        #return to main menu
    else:
        print('Enter a valid value!!')
        #repeat the qustion

def generating_password():
    pass

while True:

    #the app interface
    menu.main()
    try:
        choice = int(input('$> '))
    except ValueError:
        print('Please enter a number.')
        continue

    if choice in [1,2,3]:
        #connecting to db
        with sqlite3.connect("passwordsDataBase.db") as connect:
            cursor = connect.cursor()


        if choice == 1:
            # #checking if the db is empty
            # cursor.execute("SELECT 1 FROM passwords LIMIT 1")
            # result = cursor.fetchone()
            # if result is None:
            #     print('No saved passwords')
            # else:
            #     #Searching the db for stored passwords
            #     app, user = get_app_searching()
            #     cursor.execute("SELECT password FROM passwords WHERE app_name=? AND user_name=?", (app, user))
            #     search_res = cursor.fetchall()
            #     if search_res:
            #         print('passwords found: ')
            #         print(f'    {search_res}')
            #     else:
            #         print('No data found!!')
            pass

        elif choice == 2:
            # app, user, password = get_app()
            # cursor.execute("INSERT INTO passwords(app_name, user_name, password) VALUES (?, ?, ?)", (app, user, password))
            # print(f'Done adding the new password.')
            # connect.commit()
            #return to main menu

            pass

        elif choice == 3:
            # app, user, password = get_app()
            # qustion = input('are you sure you want to delete that password? [y/n]: ')
            # if qustion == 'y':
            #     cursor.execute("DELETE FROM passwords WHERE app_name=? AND user_name=? AND password=?", (app, user, password))
            #     print(f'the password has been deleted.')
            #     # connect.commit()
            #     #return to main menu
            # elif qustion == 'n':
            #     pass
            #     #return to main menu
            # else:
            #     print('Enter a valid value!!')
            #     #repeat the qustion
            pass

        elif choice == 4:
            pass

        elif choice == 0:
            pass
            #exit the app
        # cursor.close()
        # connect.close()
    else:
        print('Enter a valid option!!')
