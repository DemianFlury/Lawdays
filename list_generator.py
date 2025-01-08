import pulp
import csv
from collections import defaultdict, deque

def generate_list(input_path, output_path):
    # Read the CSV file
    with open(input_path, mode='r', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        attendees = list(reader)

    # Create a dictionary to store priorities
    priority_dict = defaultdict(deque)

    # Process each attendee and their priorities
    for attendee in attendees:
        name = attendee['Name']
        priorities = [attendee[f'Priority {i}'] for i in range(1, 2) if attendee[f'Priority {i}']]
        for priority in priorities:
            priority_dict[priority].append(name)

    # Create the output list respecting priorities and capacity
    output_list = []
    stand_capacity = defaultdict(int)
    max_capacity = 2

    for priority, names in priority_dict.items():
        while names and stand_capacity[priority] < max_capacity:
            name = names.popleft()
            output_list.append({'Name': name, 'Stand': priority})
            stand_capacity[priority] += 1

    # Write the output list to a new CSV file
    with open(output_path, mode='w', newline='') as csvfile:
        fieldnames = ['Name', 'Stand']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(output_list)

# Example usage
if __name__ == "__main__":
    generate_list('test.csv', 'output.csv')