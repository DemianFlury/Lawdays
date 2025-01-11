import pulp
import csv
import random

class Settings:
    def __init__(self, stands, timeslots, stand_capacity, input_path, output_path, num_priorities):
        self.stands = stands
        self.timeslots = timeslots
        self.stand_capacity = stand_capacity
        self.input_path = input_path
        self.output_path = output_path
        self.num_priorities = num_priorities

class Attendee:
    def __init__(self, name, email, priorities, major, semester):
        self.name = name
        self.email = email
        self.semester = semester
        self.major = major
        self.preferences = {priority: len(priorities) - i for i, priority in enumerate(priorities)}

def generate_list(settings):
    error_code = 0

    # Read the CSV file
    with open(settings.input_path, mode='r', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        attendees = []
        try:
            attendees = [Attendee(row['Name'], 
                              row['Email'], 
                              [row[f'Priorität{i+1}'] for i in range(settings.num_priorities)],
                              row['Studiengang'],
                              row['Semester']) for row in reader]
        except KeyError:
            error_code = 2
            return error_code

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

    # Solve the problem
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
                    break


    # Post-processing: Ensure no timeslot is empty
    for t in timeslots:
        assigned = [output[n][t - 1] for n in names if output[n][t - 1]]
        if len(assigned) < len(names):
            unassigned = [n for n in names if not output[n][t - 1]]
            available_stands = {s: settings.stand_capacity - assigned.count(s) for s in settings.stands}
            for n in unassigned:
                available_stands = {s: cap for s, cap in available_stands.items() if cap > 0 and s not in output[n]}
                if available_stands:
                    random_stand = random.choice(list(available_stands.keys()))
                    output[n][t - 1] = random_stand
                    available_stands[random_stand] -= 1
                else:
                    error_code = 1
    

    # Write the output list to a new CSV file
    with open(settings.output_path, mode='w', newline='') as csvfile:
        fieldnames = ['Name', 'Email'] + [f'Timeslot {t}' for t in timeslots] + ['Studiengang', 'Semester']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for attendee in attendees:
            row = {'Name': attendee.name, 'Email': attendee.email}
            row.update({f'Timeslot {t}': output[attendee.name][t - 1] for t in timeslots})
            row.update({'Studiengang': attendee.major, 'Semester': attendee.semester})
            writer.writerow(row)

    return error_code
