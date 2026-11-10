
# Example 8: Computer Troubleshooting
# Difficulty: Hard

power_on = input("Does the computer turn on? (yes/no): ")
display_working = input("Is anything visible on the screen? (yes/no): ")
internet_working = input("Is the internet connection working? (yes/no): ")
system_slow = input("Is the computer unusually slow? (yes/no): ")
storage_space = float(input("Enter available storage space (GB): "))

if power_on != "yes" and power_on != "no":
    print ("Invalid power status.")

elif display_working != "yes" and display_working != "no":
    print ("Invalid display status.")

elif internet_working != "yes" and internet_working != "no":
    print ("Invalid internet status.")

elif system_slow != "yes" and system_slow != "no":
    print ("Invalid performance status.")

elif storage_space < 0:
    print ("Invalid storage information.")

elif power_on == "no":
    print ("\nDIAGNOSIS: POWER-RELATED ISSUE")
    print ("Recommendation: Check the power connection and power source.")

elif display_working == "no":
    print ("\nDIAGNOSIS: DISPLAY ISSUE")
    print ("Recommendation: Check the monitor connection and display settings.")

elif internet_working == "no" and system_slow == "no":
    print ("\nDIAGNOSIS: NETWORK CONNECTIVITY ISSUE")
    print ("Recommendation: Check the router and network connection.")

elif system_slow == "yes":
    if storage_space < 5:
        print ("\nDIAGNOSIS: LOW STORAGE CAPACITY")
        print ("Recommendation: Remove unnecessary files to free up space.")

    elif storage_space <= 15:
        print ("\nDIAGNOSIS: LIMITED STORAGE CAPACITY")
        print ("Recommendation: Review storage usage and remove unneeded files.")

    else:
        print ("\nDIAGNOSIS: POSSIBLE PERFORMANCE ISSUE")
        print ("Recommendation: Check running applications and system activity.")

elif internet_working == "no":
    print("\nDIAGNOSIS: POSSIBLE NETWORK ISSUE")
    print ("Recommendation: Check network settings and connection status.")

else:
    print ("\nDIAGNOSIS: NO MAJOR ISSUE DETECTED")
    print ("The reported computer functions appear to be operating normally.")
