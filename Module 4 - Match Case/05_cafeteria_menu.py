
# Example 5: Cafeteria menu
# Difficulty: Intermediate

print ("==== CAFETERIA MENU ====")
print ("1. Chicken Meal - PHP 85")
print ("2. Burger Meal - PHP 65")
print("3. Spaghetti - PHP 55")
print ("4. Sandwich - PHP 45")

choice = int(input("\nEnter your order number: "))

match choice:
    case 1:
        item = "Chicken Meal"
        price = 85
    case 2:
        item = "Burger Meal"
        price = 65
    case 3:
        item = "Spaghetti"
        price = 55
    case 4:
        item = "Sandwich"
        price = 45
    case _:
        item = "Invalid Order"
        price = 0

print ("\n==== ORDER SUMMARY ====")
print (f"Selected Item: {item}")
print (f"Price: PHP {price:.2f}")
