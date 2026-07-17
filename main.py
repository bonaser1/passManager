import menu
import functions

functions.create_db()


if functions.check_master_password():
    menu.setting_master_password()
    try:
        master_password = functions.get_master_password()
        functions.derive_key(master_password)

    except ValueError:
        print('> Please enter a string.')
        input('\nPress Enter to continue...')
        functions.clear()

    if master_password:
        functions.set_master_password(master_password)
        functions.main_func()
else:
    functions.main_func()