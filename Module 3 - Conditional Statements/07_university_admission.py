
# Example 7: University Admission System
# Difficulty: Hard

entrance_score = float(input("Enter entrance examination score (0-100): "))
academic_average = float(input("Enter academic average (0-100): "))
program = input("Choose program (computer science/engineering/education): ")

if entrance_score < 0 or entrance_score > 100 or academic_average < 0 or academic_average > 100:
    print("Invalid academic information.")

elif program != "computer science" and program != "engineering" and program != "education":
    print("Invalid degree program.")

else:
    if program == "computer science":
        required_score = 80
        required_average = 90

    elif program == "engineering":
        required_score = 85
        required_average = 90

    else:
        required_score = 75
        required_average = 85

    if entrance_score >= required_score and academic_average >= required_average:
        print ("\nADMISSION RESULT: QUALIFIED")
        print ("The applicant satisfies all admission requirements.")

    elif entrance_score >= required_score or academic_average >= required_average:
        print ("\nADMISSION RESULT: CONDITIONAL")
        print ("The applicant satisfies only one of the two major requirements.")

    else:
        print ("\nADMISSION RESULT: NOT QUALIFIED")
        print ("The applicant does not meet the required admission standards.")

    print (f"\nChosen Program: {program}")
    print (f"Required Entrance Score: {required_score}")
    print (f"Required Academic Average: {required_average}")
