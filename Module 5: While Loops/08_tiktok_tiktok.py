# Example 8: TikTok-Tiktok
# Difficulty: Hard

creator1 = input("Enter first creator's name: ")
creator2 = input("Enter second creator's name: ")

score1 = 0
score2 = 0

print("\n==== TIKTOK LIVE GIFT BATTLE =====")
print("CREATOR 1:", creator1)
print("CREATOR 2:", creator2)

print("\n==== AVAILABLE GIFTS ====")
print("Rose          - 1 point")
print("Finger Heart  - 5 points")
print("Perfume       - 20 points")
print("Hat           - 99 points")
print("Confetti      - 100 points")
print("Sunglasses    - 199 points")
print("Galaxy        - 1,000 points")
print("Lion          - 29,999 points")
print("Universe      - 44,000 points")

print("\nType 'end' to finish the battle.")

while True:
    creator = input("\nWho received the gift? (creator 1 / creator 2): ").lower()

    if creator == "end":
        break

    elif creator == "creator 1":
        gift = input("Enter gift for " + creator1 + ": ").lower()

    elif creator == "creator 2":
        gift = input("Enter gift for " + creator2 + ": ").lower()

    else:
        print("Invalid creator! Please enter creator 1 or creator 2.")
        continue

    if gift == "rose":
        points = 1
    elif gift == "finger heart":
        points = 5
    elif gift == "perfume":
        points = 20
    elif gift == "hat":
        points = 99
    elif gift == "confetti":
        points = 100
    elif gift == "sunglasses":
        points = 199
    elif gift == "galaxy":
        points = 1000
    elif gift == "lion":
        points = 29999
    elif gift == "universe":
        points = 44000
    else:
        print("Invalid gift! Please choose from the available gifts.")
        continue

    if creator == "creator 1":
        score1 += points
        print(creator1, "received", gift, "worth", points, "points!")

    else:
        score2 += points
        print(creator2, "received", gift, "worth", points, "points!")

    print("\n==== CURRENT SCORES ====")
    print(creator1, ":", score1)
    print(creator2, ":", score2)

print("\n==== FINAL BATTLE RESULTS ====")
print(creator1, ":", score1, "points")
print(creator2, ":", score2, "points")

if score1 > score2:
    print("WINNER:", creator1)
elif score2 > score1:
    print("WINNER:", creator2)
else:
    print("The battle ended in a tie!")

print("Thank you for using the LIVE Battle Tracker!")
