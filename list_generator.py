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
    def __init__(self, name, email, priorities, major, semester, lunch, mock_interview):
        self.name = name
        self.email = email
        self.semester = semester
        self.major = major
        self.preferences = {priority: len(priorities) - i for i, priority in enumerate(priorities)}
        self.lunch = lunch
        self.mock_interview = mock_interview

def generate_list(settings):
    error_code = 0

    # Read the CSV file
    with open(settings.input_path, mode='r', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        attendees = []
        try:
            attendees = [Attendee(row['Name'], 
                              row['Email'], 
                              [row[f'Priorität {i+1}'] for i in range(settings.num_priorities)],
                              row['Studiengang'],
                              row['Semester'],
                              row['Mittagessen'],
                              row['Mock Interview']) for row in reader]
        except KeyError:
            error_code = 2
            return error_code

    # Check if any attendee has duplicate priorities
    # If so, assign a random priority to the duplicate
    for attendee in attendees:
        unique_priorities = list(set(attendee.preferences.keys()))
        while len(unique_priorities) < settings.num_priorities:
            rng = random.randint(0, len(settings.stands) - 1)
            if(settings.stands[rng] not in unique_priorities):
                unique_priorities.append(settings.stands[rng])
        attendee.preferences = {priority: settings.num_priorities - i for i, priority in enumerate(unique_priorities)}

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

    # Output results
    output = {n: [""] * len(timeslots) for n in names}
    for n in names:
        for t in timeslots:
            for s in settings.stands:
                if pulp.value(x[n][s][t]) == 1:
                    output[n][t - 1] = s
                    break

    # Write the output list to a new CSV file
    with open(settings.output_path, mode='w', newline='') as csvfile:
        fieldnames = ['Name', 'Email'] + [f'Timeslot {t}' for t in timeslots] + ['Studiengang', 'Semester', 'Mittagessen', 'Mock Interview']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for attendee in attendees:
            row = {'Name': attendee.name, 'Email': attendee.email}
            row.update({f'Timeslot {t}': output[attendee.name][t - 1] for t in timeslots})
            row.update({'Studiengang': attendee.major, 
                        'Semester': attendee.semester, 
                        'Mittagessen': attendee.lunch, 
                        'Mock Interview': attendee.mock_interview})
            writer.writerow(row)

    return error_code
