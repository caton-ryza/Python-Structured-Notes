# Example 3: Payment Method
# Difficulty: Easy

payment = input("Choose payment (cash, card, gcash): ")

match payment:
    case "cash":
        print ("Pay at the counter.")
    case "card":
        print ("Insert your card.")
    case "gcash":
        print ("Scan the payment QR code.")
    case _:
        print ("Invalid payment method.")
