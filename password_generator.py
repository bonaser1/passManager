import secrets
import string

def password_gen(length=20):
    chars = string.ascii_letters+string.digits+string.punctuation
    return ''.join(secrets.choice(chars) for _ in range(length))