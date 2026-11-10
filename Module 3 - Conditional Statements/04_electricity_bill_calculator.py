
# Example 4: Electricity Bill Calculator
# Difficulty: Hard

consumption = float(input("Enter monthly electricity consumption (kWh): "))

if consumption < 0:
    print("Invalid electricity consumption.")
else:
    if consumption <= 100:
        rate = 5.50
    elif consumption <= 200:
        rate = 6.25
    else:
        rate = 7.10

    energy_charge = consumption * rate
    service_charge = 45.00
    total_bill = energy_charge + service_charge

    print ("\n--- ELECTRICITY BILL ---")
    print (f"Consumption: {consumption:.2f} kWh")
    print (f"Rate per kWh: PHP {rate:.2f}")
    print (f"Energy Charge: PHP {energy_charge:.2f}")
    print (f"Service Charge: PHP {service_charge:.2f}")
    print (f"Total Bill: PHP {total_bill:.2f}")

    if total_bill >= 2000:
        print("Notice: Your electricity bill is relatively high.")
