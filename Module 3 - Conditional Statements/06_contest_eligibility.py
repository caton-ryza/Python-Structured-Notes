# Example 6: Personal Budget
# Difficulty: Intermediate

monthly_budget = float(input("Enter your monthly budget (PHP): "))
essential_expenses = float(input("Enter total essential expenses (PHP): "))
purchase_cost = float(input("Enter planned purchase cost (PHP): "))
minimum_savings = float(input("Enter minimum savings to preserve (PHP): "))

if monthly_budget <= 0 or essential_expenses < 0 or purchase_cost <= 0 or minimum_savings < 0:
    print("Invalid financial information.")

elif essential_expenses + minimum_savings > monthly_budget:
    print("Warning: Your essential expenses and savings exceed your budget.")

else:
    available_money = monthly_budget - essential_expenses
    remaining_after_purchase = available_money - purchase_cost

    print ("\n--- PURCHASE ASSESSMENT ---")
    print (f"Available Money: PHP {available_money:,.2f}")
    print (f"Planned Purchase: PHP {purchase_cost:,.2f}")

    if remaining_after_purchase < 0:
        print ("DECISION: PURCHASE NOT AFFORDABLE")
        print (f"Additional Money Needed: PHP {-remaining_after_purchase:,.2f}")

    elif remaining_after_purchase < minimum_savings:
        print ("DECISION: PURCHASE NOT RECOMMENDED")
        print ("Buying this item would reduce your money below your savings target.")

    else:
        print ("DECISION: PURCHASE AFFORDABLE")
        print (f"Remaining Money: PHP {remaining_after_purchase:,.2f}")
        print ("Your minimum savings target will remain protected.")
