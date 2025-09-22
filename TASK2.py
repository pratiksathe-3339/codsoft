#CALCULATOR

def get_number(prompt):
    """Get a valid number from user input."""
    while True:
        try:
            return float(input(prompt))
        except ValueError:
            print("Invalid input! Please enter a valid number.")

def get_operation():
    """Get a valid operation choice from user."""
    valid_operations = ['+', '-', '*', '/', 'add', 'subtract', 'multiply', 'divide']
    
    while True:
        operation = input("Enter operation (+, -, *, /, add, subtract, multiply, divide): ").strip().lower()
        if operation in valid_operations:
            return operation
        print("Invalid operation! Please choose from: +, -, *, /, add, subtract, multiply, divide")

def perform_calculation(num1, num2, operation):
    """Perform the calculation based on the operation."""
    # Normalize operation to symbols
    if operation in ['add', 'addition']:
        operation = '+'
    elif operation in ['subtract', 'subtraction']:
        operation = '-'
    elif operation in ['multiply', 'multiplication']:
        operation = '*'
    elif operation in ['divide', 'division']:
        operation = '/'
    
    if operation == '+':
        return num1 + num2
    elif operation == '-':
        return num1 - num2
    elif operation == '*':
        return num1 * num2
    elif operation == '/':
        if num2 == 0:
            raise ZeroDivisionError("Cannot divide by zero!")
        return num1 / num2

def display_result(num1, num2, operation, result):
    """Display the calculation result in a formatted way."""
    # Convert operation back to symbol for display
    if operation in ['add', 'addition']:
        op_symbol = '+'
    elif operation in ['subtract', 'subtraction']:
        op_symbol = '-'
    elif operation in ['multiply', 'multiplication']:
        op_symbol = '*'
    elif operation in ['divide', 'division']:
        op_symbol = '/'
    else:
        op_symbol = operation
    
    print(f"\n{'='*30}")
    print(f"Calculation: {num1} {op_symbol} {num2} = {result}")
    print(f"{'='*30}")

def main():
    """Main calculator function."""
  
    print("• Addition (+ or add)")
    print("• Subtraction (- or subtract)")
    print("• Multiplication (* or multiply)")
    print("• Division (/ or divide)")
    print()
    
    try:
        # Get user inputs
        num1 = get_number("Enter the first number: ")
        num2 = get_number("Enter the second number: ")
        operation = get_operation()
        
        # Perform calculation
        result = perform_calculation(num1, num2, operation)
        
        # Display result
        display_result(num1, num2, operation, result)
        
    except ZeroDivisionError as e:
        print(f"\nError: {e}")
    except Exception as e:
        print(f"\nAn unexpected error occurred: {e}")

def ask_continue():
    """Ask if user wants to perform another calculation."""
    while True:
        choice = input("\nWould you like to perform another calculation? (y/n): ").strip().lower()
        if choice in ['y', 'yes']:
            return True
        elif choice in ['n', 'no']:
            return False
        else:
            print("Please enter 'y' for yes or 'n' for no.")

if __name__ == "__main__":
    while True:
        main()
        if not ask_continue():
            print("\nThank you for using the calculator! Goodbye! 👋")
            break
