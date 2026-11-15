# Example 7: Student Attendance
# Difficulty: Hard

students = int(input("Enter the number of students: "))

student_number = 1
present = 0
absent = 0

while student_number <= students:
    print("\nStudent", student_number)

    attendance = input("Enter attendance (present/absent): ").lower()

    while attendance != "present" and attendance != "absent":
        print("Invalid attendance status.")
        attendance = input("Enter present or absent: ").lower()

    if attendance == "present":
        present += 1
    else:
        absent += 1

    student_number += 1

print("\nAttendance Summary")
print("Total students:", students)
print("Present:", present)
print("Absent:", absent)

if absent == 0:
    print("Perfect attendance!")
elif present > absent:
    print("Most students attended class.")
else:
    print("More students were absent than present.")
