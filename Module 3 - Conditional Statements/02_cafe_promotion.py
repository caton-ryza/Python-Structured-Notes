# Example 2: Cafe Promotion Checker
# Difficulty: Easy

total = float(input("Enter your total purchase: "))

if total >= 500:
    print ("You get a free pastry and drink!")
    
elif total >= 300:
    print ("You get a free drink!")
    
else:
    print ("No freebie for this purchase.")

print ("Thank you for visiting!") 
