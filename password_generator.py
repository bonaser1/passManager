import secrets, string
gen = ''.join(secrets.choice(string.ascii_letters+string.digits+string.punctuation)for _ in range(20))