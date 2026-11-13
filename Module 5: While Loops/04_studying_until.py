# Example 4: Studying until...
# Difficulty: Intermediate

minutes = int(input("How many minutes will you study? "))

while minutes > 0:
    print("Keep studying!")
    minutes -= 10

    if minutes > 0:
        print("Minutes remaining:", minutes)

print("Study session completed!")

