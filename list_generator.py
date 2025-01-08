import pulp
import csv

def generate_list(input_path, output_path, stand_capacity):
    # Read the CSV file
    with open(input_path, mode='r', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        attendees = list(reader)

    # Example data
    names = []
    for attendee in attendees:
        names.append(attendee['name'])
    stands = ["Stand A", "Stand B", "Stand C", "Stand D"] # TODO: read stands from settings
    timeslots = []
    for i in range(1, 4): # TODO: read amount of timeslots from settings
        timeslots.append(i)
    # timeslots = [1, 2, 3]

    # Read preferences from csv and convert to dictionary
    preferences = {}
    for attendee in attendees:
        name = attendee['name']
        preferences[name] = {}
        for stand in stands:
            if attendee['p1'] == stand:
                preferences[name][stand] = 3
            elif attendee['p2'] == stand:
                preferences[name][stand] = 2
            elif attendee['p3'] == stand:
                preferences[name][stand] = 1
            else:
                preferences[name][stand] = 0

    # Define the problem
    problem = pulp.LpProblem("Fair_Stand_Assignment", pulp.LpMaximize)

    # Define variables
    x = pulp.LpVariable.dicts("x", (names, stands, timeslots), cat="Binary")

    # Objective: Maximize total preferences
    problem += pulp.lpSum(
        preferences[n][s] * x[n][s][t] for n in names for s in stands for t in timeslots
    )

    # Constraints: One stand per attendee per timeslot
    for n in names:
        for t in timeslots:
            problem += pulp.lpSum(x[n][s][t] for s in stands) == 1
            
    # Constraints: Stand capacity per timeslot
    for s in stands:
        for t in timeslots:
            problem += pulp.lpSum(x[n][s][t] for n in names) <= stand_capacity

    # Constraint: Each attendee can visit a stand at most once across all timeslots
    for n in names:
        for s in stands:
            problem += pulp.lpSum(x[n][s][t] for t in timeslots) <= 1

    # Solve
    problem.solve()

    # Debugging output: Print the status of the solution
    print("Status:", pulp.LpStatus[problem.status])

    # Debugging output: Print the values of the decision variables
    for n in names:
        for t in timeslots:
            for s in stands:
                print(f"x[{n}][{s}][{t}] = {pulp.value(x[n][s][t])}")

    # Output results
    output = {n: [""] * len(timeslots) for n in names}
    for n in names:
        for t in timeslots:
            for s in stands:
                if pulp.value(x[n][s][t]) == 1:
                    output[n][t - 1] = s

    # Print results
    print("Name", *["Timeslot " + str(t) for t in timeslots], sep=", ")
    for n in names:
        print(n, *output[n], sep=", ")

# Example usage
if __name__ == "__main__":
    generate_list('test.csv', 'output.csv', 1)