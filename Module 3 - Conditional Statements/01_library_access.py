# Example 1: Library Access Checker
# Difficulty: Easy

account = input ("Is your library account active? ")

if account == "yes":
    books = int(input("How many books have you borrowed? "))

    if books < 5:
        print ("You can borrow another book.")
    else:
        print ("You have reached the borrowing limit.")

else:
    print ("Your account is inactive. Please visit the library.") 
