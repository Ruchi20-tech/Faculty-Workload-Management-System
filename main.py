
import pandas as pd

# Maximum weekly working hours
MAX_HOURS = 16

# Read faculty workload data from CSV
def load_workload():
    try:
        data = pd.read_csv("workload.csv")
        return data
    except FileNotFoundError:
        print("Error: workload.csv file not found!")
        return None


# Load the data
workload = load_workload()

# Stop the program if workload data cannot be loaded
if workload is None:
    raise SystemExit

 # if workload is not None:
    #print("Faculty Workload Data:")
    #print(workload) 


# Calculate total weekly hours for each faculty
def calculate_workload(data):

    totals = data.groupby("Faculty")["Hours"].sum().to_dict()

    print("\n===== WEEKLY WORKLOAD SUMMARY =====")

    for faculty, hours in totals.items():

        free_hours = MAX_HOURS - hours

        if hours > MAX_HOURS:
            print(f"{faculty}: {hours} hours - OVERLOADED by {hours - MAX_HOURS} hours")

        else:
            print(f"{faculty}: {hours} hours ({free_hours} free)")


# Display workload summary
# if workload is not None:
    #calculate_workload(workload)


# Function to assign a new subject
def assign_subject(data):

    print("\n===== ASSIGN NEW SUBJECT =====")

    faculty = input("Enter faculty name: ").strip()
    subject = input("Enter subject name: ").strip()

    try:
        hours = int(input("Enter weekly hours: "))

        if hours <= 0:
            print("Hours must be a positive whole number.")
            return data

    except ValueError:
        print("Invalid input! Hours must be a whole number.")
        return data

    if not faculty or not subject:
        print("Faculty name and subject cannot be empty.")
        return data

    if faculty not in data["Faculty"].values:
        print("Faculty member not found!")
        return data
    if subject in data.loc[data["Faculty"] == faculty, "Subject"].values:
      print("This subject is already assigned to this faculty member!")
      return data

   

    current_hours = data.loc[
        data["Faculty"] == faculty, "Hours"
    ].sum()

    if current_hours + hours > MAX_HOURS:
        print("\nCannot assign subject!")
        print("Current workload:", current_hours)
        print("New total:", current_hours + hours)
        print("Maximum allowed:", MAX_HOURS)
        return data

    new_subject = pd.DataFrame({
        "Faculty": [faculty],
        "Subject": [subject],
        "Hours": [hours]
    })

    data = pd.concat([data, new_subject], ignore_index=True)

    data.to_csv("workload.csv", index=False)

    print("\nSubject assigned successfully!")
    print("Updated workload:", current_hours + hours)
    print("Remaining free hours:", MAX_HOURS - current_hours - hours)

    return data


# Take input and assign a subject
 #if workload is not None:
    # workload = assign_subject(workload)


# Function to find available faculty
def find_available_faculty(data):

    print("\n===== FIND AVAILABLE FACULTY =====")

    try:
        required_hours = int(input("Enter required hours: "))

        if required_hours <= 0:
            print("Hours must be positive.")
            return

    except ValueError:
        print("Invalid input! Enter a whole number.")
        return

    totals = data.groupby("Faculty")["Hours"].sum()

    print("\nAvailable Faculty:")

    found = False

    for faculty, hours in totals.items():

        free_hours = MAX_HOURS - hours

        if free_hours >= required_hours:
            print(f"{faculty}: {free_hours} hours free")
            found = True

    if not found:
        print("No faculty members have sufficient free hours.")

# Main Menu
while True:

    print("\n===== FACULTY WORKLOAD MANAGEMENT SYSTEM =====")
    print("1. Show Workload Summary")
    print("2. Assign New Subject")
    print("3. Find Faculty with Free Hours")
    print("4. Exit")

    choice = input("\nEnter your choice: ")

    if choice == "1":
        calculate_workload(workload)

    elif choice == "2":
        workload = assign_subject(workload)

    elif choice == "3":
        find_available_faculty(workload)

    elif choice == "4":
        print("Exiting Faculty Workload Management System.")
        break

    else:
        print("Invalid choice! Please enter 1, 2, 3, or 4.")