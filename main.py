import menu
import database
import password_generator as pg




while True:
    
    #Starting app interface
    # database.clear()
    menu.main()

    #processing user choices
    try:
        choice = database.get_choice()

    except ValueError:
        print('Please enter a number.')
        continue
    
    if choice == 1:
        database.search_passwords()

    elif choice == 2:
        database.add_password()

    elif choice == 3:
        database.delete_password()

    elif choice == 4:
        print(pg.password_gen())

    elif choice == 0:
        break

    else:
        print('Enter a valid option!!')
