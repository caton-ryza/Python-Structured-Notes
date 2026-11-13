# Example 8: Aquarium Exhibit
# Difficulty: Hard


print ("===== AQUARIUM EXHIBITS =====")
print ("1. Coral Reef")
print ("2. Shark Zone")
print ("3. Jellyfish Gallery")
print ("4. Deep Sea")

exhibit = int(input("Choose an exhibit number: "))

match exhibit:
    case 1:
        print ("\nExhibit: Coral Reef")
        print ("Featured Animal: Clownfish")
        print ("Water Type: Saltwater")
        print ("Fun Fact: Coral reefs support many marine species.")

    case 2:
        print ("\nExhibit: Shark Zone")
        print ("Featured Animal: Great White Shark")
        print ("Water Type: Saltwater")
        print ("Fun Fact: Sharks have been around for millions of years.")

    case 3:
        print ("\nExhibit: Jellyfish Gallery")
        print ("Featured Animal: Moon Jellyfish")
        print ("Water Type: Saltwater")
        print ("Fun Fact: Jellyfish have no bones.")

    case 4:
        print ("\nExhibit: Deep Sea")
        print ("Featured Animal: Anglerfish")
        print ("Water Type: Deep Ocean")
        print ("Fun Fact: Some anglerfish use a glowing lure.")

    case _:
        print ("Invalid exhibit number.")
