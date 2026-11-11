# Example 6: School Subject
# Difficulty: Intermediate

print ("==== SUBJECT LIST ====")
print ("1. Programming")
print ("2. Mathematics")
print ("3. Science")
print ("4. English")

choice = int(input("Choose a subject: "))

match choice:
    case 1:
        subject = "Programming"
        teacher = "Mr. Reyes"
        room = "Computer Laboratory"
    case 2:
        subject = "Mathematics"
        teacher = "Ms. Cruz"
        room = "Room 201"
    case 3:
        subject = "Science"
        teacher = "Mr. Santos"
        room = "Science Laboratory"
    case 4:
        subject = "English"
        teacher = "Ms. Garcia"
        room = "Room 105"
    case _:
        subject = "Unknown"
        teacher = "None"
        room = "None"

if subject != "Unknown":
    print (f"\nSubject: {subject}")
    print (f"Teacher: {teacher}")
    print (f"Location: {room}")
else:
    print ("Invalid subject choice.")
