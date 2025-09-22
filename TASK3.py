import random
import string

def generate_password():
    """
    Generates a secure password based on user-specified length and complexity.
    """
    # 1. Define the character sets to be used
    letters = string.ascii_letters  # Contains 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
    digits = string.digits          # Contains '0123456789'
    symbols = string.punctuation    # Contains '!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~'

    # 2. Get user input for password length with error handling
    while True:
        try:
            length = int(input("Enter the desired password length (minimum 8): "))
            if length >= 8:
                break
            else:
                print("Password length must be at least 8 characters.")
        except ValueError:
            print("Invalid input. Please enter a number.")

    # 3. Get user input for complexity
    include_digits = input("Include digits? (y/n): ").lower() == 'y'
    include_symbols = input("Include special symbols? (y/n): ").lower() == 'y'

    # 4. Create the character pool based on user's choice
    char_pool = letters
    if include_digits:
        char_pool += digits
    if include_symbols:
        char_pool += symbols

    # 5. Generate the password
    # This method ensures that at least one of each chosen character type is included
    password_list = []
    
    # Always include at least one uppercase and one lowercase letter
    password_list.append(random.choice(string.ascii_lowercase))
    password_list.append(random.choice(string.ascii_uppercase))

    if include_digits:
        password_list.append(random.choice(digits))
    if include_symbols:
        password_list.append(random.choice(symbols))

    # Fill the rest of the password length with random characters from the pool
    remaining_length = length - len(password_list)
    for _ in range(remaining_length):
        password_list.append(random.choice(char_pool))

    # Shuffle the list to ensure the characters are in a random order
    random.shuffle(password_list)

    # Join the list of characters into a final string
    password = "".join(password_list)

    # 6. Display the password
    print("\n" + "="*25)
    print(" Your Generated Password Is")
    print("="*25)
    print(f"->  {password}")
    print("="*25 + "\n")

# Run the password generator
if __name__ == "__main__":
    generate_password()