import pulp
import csv

class Settings:
    def __init__(self, stands, timeslots, stand_capacity, input_path, output_path):
        self.stands = stands
        self.timeslots = timeslots
        self.stand_capacity = stand_capacity
        self.input_path = input_path
        self.output_path = output_path

class Attendee:
    def __init__(self, name, email, p1, p2, p3, major, semester):
        self.name = name
        self.email = email
        self.semester = semester
        self.major = major
        self.preferences = {
            p1: 3,
            p2: 2,
            p3: 1
        }

def generate_list(settings):
    # Read the CSV file
    with open(settings.input_path, mode='r', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        attendees = [Attendee(row['name'], 
                              row['email'], 
                              row['p1'], 
                              row['p2'], 
                              row['p3'],
                              row['studiengang'],
                              row['semester']) for row in reader]

    # Example data
    names = [attendee.name for attendee in attendees]
    timeslots = list(range(1, settings.timeslots + 1))

    # Define the problem
    problem = pulp.LpProblem("Fair_Stand_Assignment", pulp.LpMaximize)

    # Define variables
    x = pulp.LpVariable.dicts("x", (names, settings.stands, timeslots), cat="Binary")

    # Objective: Maximize total preferences
    problem += pulp.lpSum(
        attendee.preferences.get(stand, 0) * x[attendee.name][stand][t]
        for attendee in attendees for stand in settings.stands for t in timeslots
    )

    # Constraints: One stand per attendee per timeslot
    for n in names:
        for t in timeslots:
            problem += pulp.lpSum(x[n][s][t] for s in settings.stands) <= 1

    # Constraints: Stand capacity per timeslot
    for s in settings.stands:
        for t in timeslots:
            problem += pulp.lpSum(x[n][s][t] for n in names) <= settings.stand_capacity

    # Constraint: Each attendee can visit a stand at most once across all timeslots
    for n in names:
        for s in settings.stands:
            problem += pulp.lpSum(x[n][s][t] for t in timeslots) <= 1

    # Solve
    problem.solve()

    # Debugging output: Print the status of the solution
    print("Status:", pulp.LpStatus[problem.status])

    # Debugging output: Print the values of the decision variables
    for n in names:
        for t in timeslots:
            for s in settings.stands:
                print(f"x[{n}][{s}][{t}] = {x[n][s][t].varValue}")

    # Output results
    output = {n: [""] * len(timeslots) for n in names}
    for n in names:
        for t in timeslots:
            for s in settings.stands:
                if pulp.value(x[n][s][t]) == 1:
                    output[n][t - 1] = s

    # Write the output list to a new CSV file
    with open(settings.output_path, mode='w', newline='') as csvfile:
        fieldnames = ['Name', 'Email'] + [f'Timeslot {t}' for t in timeslots] + ['Studiengang', 'Semester']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for attendee in attendees:
            row = {'Name': attendee.name, 'Email': attendee.email}
            row.update({f'Timeslot {t}': output[attendee.name][t - 1] for t in timeslots})
            row.update({f'Studiengang': attendee.major, 'Semester': attendee.semester})
            writer.writerow(row)

# Example usage
if __name__ == "__main__":
    settings = Settings(stands=["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k"],
                        timeslots=3,
                        stand_capacity=12,
                        input_path='test.csv',
                        output_path='output.csv')
    generate_list(settings)
