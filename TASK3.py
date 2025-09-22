import random
import string

def generate_password():
    """
    Generates a secure password based on user-specified length and complexity.
    """
    
    letters = string.ascii_letters  
    digits = string.digits          
    symbols = string.punctuation    
    while True:
        try:
            length = int(input("Enter the desired password length (minimum 8): "))
            if length >= 8:
                break
            else:
                print("Password length must be at least 8 characters.")
        except ValueError:
            print("Invalid input. Please enter a number.")

    
    include_digits = input("Include digits? (y/n): ").lower() == 'y'
    include_symbols = input("Include special symbols? (y/n): ").lower() == 'y'

    
    char_pool = letters
    if include_digits:
        char_pool += digits
    if include_symbols:
        char_pool += symbols

    
    password_list = []
    
    
    password_list.append(random.choice(string.ascii_lowercase))
    password_list.append(random.choice(string.ascii_uppercase))

    if include_digits:
        password_list.append(random.choice(digits))
    if include_symbols:
        password_list.append(random.choice(symbols))

    
    remaining_length = length - len(password_list)
    for _ in range(remaining_length):
        password_list.append(random.choice(char_pool))

    
    random.shuffle(password_list)

    
    password = "".join(password_list)

    
    print("\n" + "="*25)
    print(" Your Generated Password Is")
    print("="*25)
    print(f"->  {password}")
    print("="*25 + "\n")


if __name__ == "__main__":

    generate_password()
