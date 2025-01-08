import pulp
import csv

def generate_list(input_path, output_path):
    # Read the CSV file
    with open(input_path, mode='r', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        attendees = list(reader)

    # Example data
    names = ["Alice", "Bob", "Charlie"] # TODO: read names from csv
    stands = ["Stand A", "Stand B", "Stand C", "Stand D"] # TODO: read stands from settings
    timeslots = []
    for i in range(1, 4): # TODO: read amount of timeslots from settings
        timeslots.append(i)
    # timeslots = [1, 2, 3]

    # TODO: read preferences from csv and convert to dictionary
    # Priority scores: attendee -> stand
    preferences = {
        "Alice": {"Stand A": 0, "Stand B": 2, "Stand C": 1, "Stand D": 3},
        "Bob": {"Stand A": 2, "Stand B": 3, "Stand C": 0, "Stand D": 1},
        "Charlie": {"Stand A": 3, "Stand B": 2, "Stand C": 1, "Stand D": 0},
    }

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
            problem += pulp.lpSum(x[n][s][t] for s in stands) <= 1 # TODO: read stand capacity from settings

    # Constraints: Optional stand capacity (e.g., 2 per stand per timeslot)
    stand_capacity = 1
    for s in stands:
        for t in timeslots:
            problem += pulp.lpSum(x[n][s][t] for n in names) <= stand_capacity

    # Constraint: Each attendee can visit a stand at most once across all timeslots
    for n in names:
        for s in stands:
            problem += pulp.lpSum(x[n][s][t] for t in timeslots) <= 1

    # Solve
    problem.solve()

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
    generate_list('test.csv', 'output.csv')