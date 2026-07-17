# 🔐 Password Manager CLI

A secure command-line password manager written in Python that stores credentials in an encrypted SQLite database.

The application uses **bcrypt** to securely hash the master password and **Fernet encryption (AES-128)** with a key derived from the master password using **PBKDF2-HMAC-SHA256** to protect stored passwords.

---

## Features

- Secure master password authentication
- Password hashing using bcrypt
- Encryption using Fernet
- PBKDF2 key derivation with random salt
- Store website credentials securely
- Search passwords by domain
- View or copy passwords to clipboard
- Edit existing passwords
- Delete saved passwords
- Generate strong random passwords
- Change the master password while preserving encrypted data
- SQLite database for local storage
- Simple command-line interface

---

## Technologies Used

- Python 3
- SQLite3
- bcrypt
- cryptography
- pyperclip

---

## Project Structure

```
PasswordManager/
│
├── main.py
├── functions.py
├── menu.py
├── passwordsDataBase.db
├── salt.bin
├── requirements.txt
├── README.md
└── .gitignore
```

---

## Security

This project follows several security best practices:

- Master passwords are **never stored in plain text**.
- Passwords are hashed using **bcrypt**.
- Encryption keys are **derived** from the master password using **PBKDF2-HMAC-SHA256**.
- Every password stored in the vault is encrypted using **Fernet symmetric encryption**.
- A randomly generated salt is stored separately to prevent rainbow-table attacks.
- Changing the master password automatically decrypts and re-encrypts all stored credentials with the new key.

---

## Installation

Clone the repository.

```bash
git clone https://github.com/bonaser1/passwordManager_CLI.git
```

Move into the project folder.

```bash
cd passwordManager_CLI
```

Install the dependencies.

```bash
pip install -r requirements.txt
```

Run the application.

```bash
python main.py
```

---

## Usage

On first launch:

- Create a master password.
- The application creates the database.
- A random cryptographic salt is generated.
- The master password is securely hashed.

After logging in you can:

- Search passwords
- Save new passwords
- Delete passwords
- Generate secure passwords
- Change the master password

---

## Future Improvements

- GUI version
- Password strength checker
- Import / Export encrypted vault
- Automatic backups
- Tags and categories
- Search by username
- Auto-lock after inactivity
- Unit tests
- Logging
- Cross-platform executable

---

## Learning Goals

This project was built to practice:

- Python programming
- Object organization and modular code
- SQLite databases
- Password hashing
- Symmetric encryption
- Cryptographic key derivation
- Error handling
- Secure application design

---

## Disclaimer

This project was created for educational and portfolio purposes.

Although it follows modern security practices, it has not been professionally audited and should not be relied upon for protecting highly sensitive information.

---

## Author

Ahmed Nasser

GitHub: https://github.com/bonaser1