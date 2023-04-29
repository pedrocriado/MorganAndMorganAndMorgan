import csv
from faker import Faker
import random
import datetime
import pytz

# Create a Faker object to generate fake data
fake = Faker()

# Set the number of users and events to generate
num_users = 10
num_events = 100

# Define the CSV file headers
headers = ['username', 'email', 'event_title', 'start_time', 'end_time']

# Create a list to store the event data
event_data = []

# Generate data for each user
for user_id in range(num_users):
    # Generate user-specific data
    username = fake.user_name()
    email = fake.email()
    timezone = fake.timezone()
    timezone_obj = pytz.timezone(timezone)  # get timezone object from string
    
    # Generate calendar events for the user
    for event_id in range(num_events):
        # Generate event-specific data
        event_title = fake.sentence(nb_words=4, variable_nb_words=True)
        event_start = fake.date_time_between(start_date="-30d", end_date="+30d", tzinfo=timezone_obj)  # use timezone_obj
        event_duration = datetime.timedelta(minutes=random.randint(15, 240))
        event_end = event_start + event_duration
        
        # Add the event data to the list
        event_data.append([username, email, event_title, event_start, event_end])

# Write the event data to a CSV file
with open('calendar_data.csv', mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(headers)
    writer.writerows(event_data)
