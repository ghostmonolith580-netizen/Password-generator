import random
import string

def generate_password(length=12):
    # Define the possible characters: letters, digits, and punctuation
    characters = string.ascii_letters + string.digits + string.punctuation
    
    # Randomly pick characters from the pool
    password = ''.join(random.choice(characters) for _ in range(length))
    
    return password

# Quick test
if __name__ == "__main__":
    print("Your new password is:", generate_password(16))