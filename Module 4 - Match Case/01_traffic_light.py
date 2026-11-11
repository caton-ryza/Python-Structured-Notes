# Example 2: Traffic Light
# Difficulty: Easy

light = input("Enter traffic light color: ")

match light:
    case "Red":
        print ("Stop!")
    case "Yellow":
        print ("Get ready!")
    case "Green":
        print ("Go!")
    case _:
        print ("Invalid color.")
