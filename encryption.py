from cryptography.fernet import Fernet
from pathlib import Path

KEY_FILE = Path("secret.key")

def generate_and_save_key(): 
    if KEY_FILE.exists():
        return
    key = Fernet.generate_key()
    with open("secret.key", "wb") as key_file:
        key_file.write(key)
    print("Encryption key generated and saved as 'secret.key'.")

def load_key():
    return open("secret.key", "rb").read()

def encrypt_password(password: str) -> str:
    key = load_key()
    f = Fernet(key)
    encrypted_bytes = f.encrypt(password.encode())
    return encrypted_bytes.decode()

def decrypt_password(encrypted_password: str) -> str:
    key = load_key()
    f = Fernet(key)
    decrypted_bytes = f.decrypt(encrypted_password.encode())
    return decrypted_bytes.decode()

