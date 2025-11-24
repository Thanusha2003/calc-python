def calculator():
    print("Simple Python Calculator")
    print("------------------------")
    print("Select an operation:")
    print("1. Add")
    print("2. Subtract")
    print("3. Multiply")
    print("4. Divide")

    choice = input("Enter your choice (1-4): ")

    if choice not in ['1', '2', '3', '4']:
        print("Invalid choice! Please run the program again.")
        return

    try:
        num1 = float(input("Enter first number: "))
        num2 = float(input("Enter second number: "))
    except ValueError:
        print("Invalid number! Please enter digits only.")
        return

    if choice == '1':
        result = num1 + num2
        op = "+"
    elif choice == '2':
        result = num1 - num2
        op = "-"
    elif choice == '3':
        result = num1 * num2
        op = "*"
    elif choice == '4':
        if num2 == 0:
            print("Error: Cannot divide by zero.")
            return
        result = num1 / num2
        op = "/"

    print(f"\nResult: {num1} {op} {num2} = {result}")


# Run the calculator
calculator()
