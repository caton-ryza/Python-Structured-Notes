
# Example 4: Calculator Operation
# Difficulty: Intermediate

first_number = float(input("Enter first number: "))
second_number = float(input("Enter second number: "))

operation = input("Choose operation (+, -, *, /): ")

match operation:
    case "+":
        result = first_number + second_number
    case "-":
        result = first_number - second_number
    case "*":
        result = first_number * second_number
    case "/":
        if second_number != 0:
            result = first_number / second_number
        else:
            result = None
            print ("Cannot divide by zero.")
    case _:
        result = None
        print ("Invalid operation.")

if result != None:
    print (f"Result: {result}")
