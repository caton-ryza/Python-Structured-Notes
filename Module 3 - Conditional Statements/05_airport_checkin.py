
# Example 5: Airport Check-in Assessment
# Difficulty: Intermediate

hours_before_departure = float(input("Hours remaining before departure: "))
documents_ready = input("Are travel documents complete? (yes/no): ")
baggage_weight = float(input("Enter baggage weight (kg): "))

if hours_before_departure < 0 or baggage_weight < 0:
    print("Invalid passenger information.")

elif hours_before_departure < 1:
    print("Check-in closed. Passenger cannot proceed.")

elif documents_ready == "no":
    print("Check-in denied: Incomplete travel documents.")

elif documents_ready != "yes":
    print("Invalid document response.")

else:
    if baggage_weight <= 20:
        print("\nCHECK-IN APPROVED")
        print("Baggage is within the standard weight limit.")

    elif baggage_weight <= 30:
        print("\nCHECK-IN APPROVED WITH ADDITIONAL FEE")
        print("Passenger must pay the excess baggage charge.")

    else:
        print("\nCHECK-IN ON HOLD")
        print("Baggage exceeds the permitted weight limit.")
