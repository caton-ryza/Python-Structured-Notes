# Example 7: Mood Activity Recommender
# Difficulty: Hard

print ("==== MOOD ACTIVITY RECOMMENDER ====")
print ("Moods: happy, sad, stressed, bored")
print ("Free time: short, long")

mood = input ("How are you feeling? ")
free_time = input ("Do you have short or long free time? ")

match mood:
    case "happy":
        match free_time:
            case "short":
                print ("Suggestion: Listen to your favorite songs.")
            case "long":
                print ("Suggestion: Go out with your friends.")
            case _:
                print ("Invalid free time.")

    case "sad":
        match free_time:
            case "short":
                print ("Suggestion: Watch a comforting video.")
            case "long":
                print ("Suggestion: Watch your favorite movie.")
            case _:
                print ("Invalid free time.")

    case "stressed":
        match free_time:
            case "short":
                print ("Suggestion: Take a quiet break.")
            case "long":
                print ("Suggestion: Spend time on a relaxing hobby.")
            case _:
                print ("Invalid free time.")

    case "bored":
        match free_time:
            case "short":
                print ("Suggestion: Play a quick game.")
            case "long":
                print ("Suggestion: Try learning something new.")
            case _:
                print ("Invalid free time.")

    case _:
        print ("Mood not recognized.")
