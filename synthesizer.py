import random
import csv
import datetime

# Define users
users = ['user' + str(i) for i in range(1, 101)]

# Define event types
event_types = ['Meeting', 'Lunch', 'Presentation', 'Training', 'Appointment']

# Define start and end dates
start_date = datetime.date(2023, 5, 1)
end_date = datetime.date(2023, 5, 31)

# Generate events for each user
events = []
for user in users:
    for i in range(5):
        # Choose a random event type
        event_type = random.choice(event_types)
        
        # Choose a random start and end time
        start_time = datetime.datetime.combine(start_date, datetime.time(random.randint(9, 16), 0))
        end_time = start_time + datetime.timedelta(hours=random.randint(1, 3))
        
        # Add event details to list
        events.append([user, event_type, start_time.date(), start_time.time(), end_time.time()])

# Write events to CSV file
with open('calendar_events.csv', mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['User', 'Event Type', 'Date', 'Start Time', 'End Time'])
    for event in events:
        writer.writerow(event)
