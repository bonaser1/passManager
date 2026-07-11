import menu
import database
import password_generator as pg


database.create_db()
pg.generate_and_save_key()

while True:

    if database.first_time():
        menu.seting_master_password()
        try:
            master_password = database.get_master_password()

        except ValueError:
            print('Please enter a string.')
            continue

        if master_password:
            database.set_master_password(master_password)
    else:

        menu.checking_master_password()
        plain_password = database.get_master_password()
        if database.check_master_password(plain_password):
        
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
                menu.change_master_password()
                plain_password = database.get_master_password()
                database.change_master_password(plain_password)

            elif interface3_choice == 0:
                break

            else:
                print('Enter a valid option!!')
        else:
            continue
