# Example 1: Weather Description
# Difficulty: Easy

weather = input("Enter the weather (sunny, rainy, cloudy): ")

match weather:
    case "sunny":
        print ("It's a good day to go outside!")
    case "rainy":
        print ("Bring an umbrella!")
    case "cloudy":
        print ("The sky is covered with clouds.")
    case _:
        print ("Unknown weather condition.")
