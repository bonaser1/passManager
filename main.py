import menu
import functions

functions.create_db()


if functions.check_master_password():
    while True:
        menu.setting_master_password()
        master_password = functions.get_master_password()
        
        if not master_password:
            functions.error("> Master password cannot be empty.")
            continue

        functions.derive_key(master_password)
        functions.set_master_password(master_password)
        break

functions.main_func()