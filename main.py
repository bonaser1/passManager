import menu
import database
import password_generator as pg

while True:

    #the app interface
    menu.main()
    try:
        choice = database.get_choice() # int(input('$> '))
    except ValueError:
        print('Please enter a number.')
        continue

    if choice in (0,1,2,3,4):
            if choice == 1:
                database.search_passwords()

            elif choice == 2:
                database.add_password()

            elif choice == 3:
                database.delete_password()

            elif choice == 4:
                print(pg.gen)

            elif choice == 0:
                break
    else:
        print('Enter a valid option!!')
