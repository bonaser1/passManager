import menu
import database
import encryption
from colorama import Fore

database.create_db()
encryption.generate_and_save_key()

def main_func():
    while True:
        menu.checking_master_password()
        plain_password = database.get_master_password()
        if database.check_master_password(plain_password):
            break
        print(Fore.RED + "> Incorrect master password. Please try again.")
    while True:
        #Starting app interface
        # database.clear()
        menu.main()

        #processing user choices
        try:
            interface3_choice = database.get_choice()

        except ValueError:
            print('Please enter a number.')
            continue
        
        if interface3_choice == 1:
            database.search_passwords()

        elif interface3_choice == 2:
            database.add_password()

        elif interface3_choice == 3:
            database.delete_password()

        elif interface3_choice == 4:
            database.generate_password()

        elif interface3_choice == 5:
            database.change_master_password_flow()
                    
                

        elif interface3_choice == 0:
            break

        else:
            print('Enter a valid option!!')

if database.first_time():
    menu.seting_master_password()
    try:
        master_password = database.get_master_password()

    except ValueError:
        print('Please enter a string.')

    if master_password:
        database.set_master_password(master_password)
        main_func()
else:
    main_func()