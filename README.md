# Password Manager

A secure command-line password manager application built with Python. This application allows users to securely store, retrieve, generate, and manage passwords with encryption and a master password protection system.

## Features

- 🔐 **Master Password Protection**: Set and verify a master password on first launch
- 🔑 **Secure Password Storage**: Passwords are encrypted using Fernet encryption
- 🔍 **Search & Retrieve**: Look up stored passwords by domain name
- ➕ **Add Passwords**: Store new passwords with associated domain and username
- ❌ **Delete Passwords**: Remove unwanted password entries
- 🎲 **Generate Passwords**: Automatically generate strong random passwords
- 📋 **Copy to Clipboard**: Quickly copy passwords to your clipboard
- ✏️ **Edit Passwords**: Modify existing password entries
- 🔑 **Change Master Password**: Update your master password with verification
- 💾 **SQLite Database**: Local database storage for all passwords

## Project Structure

```
passManager/
├── main.py                 # Application entry point
├── functions.py            # Core functionality and database operations
├── menu.py                 # CLI menu interfaces
├── encryption.py           # Encryption/decryption utilities
├── password_generator.py    # Password generation module
├── passwordsDataBase.db     # SQLite database (created on first run)
└── secret.key             # Encryption key (created on first run)
```

## Requirements

- Python 3.x
- `pyperclip` - For clipboard operations
- `bcrypt` - For password hashing
- `cryptography` - For Fernet encryption

## Installation

1. Clone the repository:
```bash
git clone https://github.com/bonaser1/passManager.git
cd passManager
```

2. Install required dependencies:
```bash
pip install pyperclip bcrypt cryptography
```

## Usage

Start the application:
```bash
python main.py
```

### First Launch

On the first launch, you will be prompted to set a master password. This password protects access to all your stored passwords.

### Main Menu Options

1. **Search for a Password** - Look up passwords by domain name
2. **Save a New Password** - Add a new password entry
3. **Delete a Password** - Remove a password entry
4. **Generate a Password** - Create a strong random password
5. **Change Master Password** - Update your master password
6. **Exit** - Close the application

### Password Operations

When searching for a password, you can:
- **[C]** Copy password to clipboard
- **[V]** View password on screen
- **[D]** Delete the password
- **[E]** Edit the password

## Security Features

- **Master Password Hashing**: Master password is hashed using bcrypt for secure storage
- **Fernet Encryption**: Individual passwords are encrypted using Fernet symmetric encryption
- **Encryption Key**: A unique encryption key is generated and stored in `secret.key`
- **Local Storage**: All data is stored locally on your machine

## Warning

⚠️ **Important Security Notes:**

- Keep your `secret.key` file safe - it's required to decrypt your passwords
- Back up your encryption key and database file
- Never share your master password
- This is a local application - data is not synced to the cloud

## Version

Current Version: v0.2

## Future Improvements

- Add master password strength validation
- Implement password history/recovery
- Add support for password categories/tags
- Create GUI interface
- Add password expiration reminders
- Implement backup/restore functionality

## License

This project is open source and available under the MIT License.

## Author

Created by bonaser1

---

**Disclaimer**: This password manager is provided as-is for educational purposes. Always ensure you have backups of your important passwords and encryption keys.
