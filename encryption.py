from cryptography.fernet import Fernet
from pathlib import Path

KEY_FILE = Path("secret.key")

def generate_and_save_key(): 
    if KEY_FILE.exists():
        return
    #Generates a key and saves it to a file.
    key = Fernet.generate_key()
    with open("secret.key", "wb") as key_file:
        key_file.write(key)
    print("Encryption key generated and saved as 'secret.key'.") # 

def load_key():
    #Loads the encryption key from the current directory.
    return open("secret.key", "rb").read()

def encrypt_password(password: str) -> str:
    #Encrypts a password using Fernet symmetric encryption.
    key = load_key()
    f = Fernet(key)
    # Encrypt the password and decode it to a string for DB storage
    encrypted_bytes = f.encrypt(password.encode())
    return encrypted_bytes.decode()

def decrypt_password(encrypted_password: str) -> str:
    #Decrypts an encrypted password string.
    key = load_key()
    f = Fernet(key)
    # Decrypt and decode back to plaintext
    decrypted_bytes = f.decrypt(encrypted_password.encode())
    return decrypted_bytes.decode()