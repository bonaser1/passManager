import menu
import functions

functions.create_db()
functions.generate_and_save_key()

if functions.check_master_password():
    menu.seting_master_password()
    try:
        master_password = functions.get_master_password()

    except ValueError:
        print('> Please enter a string.')
        input('\nPress Enter to continue...')
        functions.clear()

    if master_password:
        functions.set_master_password(master_password)
        functions.main_func()
else:
    functions.main_func()