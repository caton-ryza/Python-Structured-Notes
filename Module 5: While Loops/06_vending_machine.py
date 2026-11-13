# Example 6: Vending Machine
# Difficulty: Intermediate

balance = 100

while balance > 0:
    print("\nAvailable balance:", balance)
    price = int(input("Enter the price of your item (0 to stop): "))

    if price == 0:
        print("Transaction ended.")
        break
    elif price < 0:
        print("Invalid price.")
    elif price <= balance:
        balance -= price
        print("Purchase successful!")
    else:
        print("Not enough balance.")

print("Remaining balance:", balance)
