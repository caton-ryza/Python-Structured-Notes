# Example 3: Battery Saver Recommendation
# Difficulty: Easy

battery = int(input("Enter battery percentage: "))

if battery <= 15:
  print ("Critical battery!")
  print ("Turn on power saving mode.")
elif battery <= 40:
  print ("Battery is getting low.")
  print ("Consider charging your device.")
elif battery <= 70:
  print ("Battery level is moderate.")
else:
  print ("Battery level is good.")
  
