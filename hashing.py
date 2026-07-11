import bcrypt

def login_user(username, input_password):
    """Fetches the hash from the database and verifies the password."""
    # Check if user exists
    if username not in database:
        return False
        
    # Get the stored hash from the database
    stored_hash = database[username]
    
    # Convert input string to bytes
    input_bytes = input_password.encode('utf-8')
    
    # Verify and return True or False
    return bcrypt.checkpw(input_bytes, stored_hash)


# --- USAGE ---

# 1. Register a new user
register_user("alice_dev", "MySecurePass123!")

# 2. Try to log in
is_success = login_user("alice_dev", "MySecurePass123!")
print("Login successful:", is_success) # Returns True