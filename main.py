import secrets, string, sqlite3

#the app interface
print('Password Manager App v0.1\n')
print('         [1] Looking for a password?')
print('         [2] Saving a password?')
print('         [3] Deleting a password?')
print('         [4] Genreating a password?')
print('         [0] Exit')
choice = input('$> ')

if choice in [1,2,3]:
    #connecting to db
    connect = sqlite3.connect('\passwordsDataBase.db')
    cursor = connect.cursor()

    if choice == 1:
        #checking if the db is empty
        cursor.execute("SELECT 1 FROM passwords LIMIT 1")
        result = cursor.fetchone()
        if result is None:
            print('No saved passwords')
        else:
            #Searching the db for stored passwords
            app_name = input('Enter the app name: ')
            user_name = input('Enter the username: ')
            cursor.excute("SELECT password FROM passwords WHERE app_name=? AND user_name=?", (app_name, user_name))
            search_res = cursor.fetchall()
            if search_res:
                print('passwords found: ')
                print(f'    {search_res}')
            else:
                print('No data found!!')

    elif choice == 2:
        app_name = input('Enter the app name: ')
        user_name = input('Enter the username: ')
        pass_w = input('Enter the password: ')
        cursor.execute("INSERT INTO passwords(app_name, user_name, password) VALUES (?, ?, ?)", (app_name, user_name, pass_w))
        print(f'Done adding {app_name}\'s new password.')
        #return to main menu

    elif choice == 3:
        app_name = input('Enter the app name: ')
        user_name = input('Enter the username: ')
        pass_w = input('Enter the password: ')
        qustion = input('are you sure you want to delete that password? [y/n]: ')
        if qustion == 'y':
            cursor.execute("DELETE * FROM passwords WHERE app_name=? AND user_name=? AND password=?", (app_name, user_name, pass_w))
            print(f'{app_name}\'s password has been deleted.')
            #return to main menu
        elif qustion == 'n':
            pass
            #return to main menu
        else:
            print('Enter a valid value!!')
            #repeat the qustion

    elif choice == 4:
        pass

    elif choice == 0:
        pass
        #exit the app

else:
    print('Enter a valid option!!')
