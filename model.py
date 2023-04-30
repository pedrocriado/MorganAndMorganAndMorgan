import torch
import random
import datetime
import csv

# Define users
users = ['user' + str(i) for i in range(1, 101)]

# Define event types
event_types = ['Meeting', 'Lunch', 'Presentation', 'Training', 'Appointment']

# Define start and end dates
start_date = datetime.date(2023, 5, 1)
end_date = datetime.date(2023, 5, 31)

# Define the number of MCMC iterations
num_iterations = 10000

# Define the temperature parameter
temperature = 0.1

# Define the schedule tensor
schedule = torch.zeros(len(users), 31, 8)

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
        events.append({'user': user, 'event_type': event_type, 'date': start_time.date(), 'start_time': start_time.time(), 'end_time': end_time.time()})

# Assign events to initial schedule
for event in events:
    user_index = users.index(event['user'])
    date_index = (event['date'] - start_date).days
    start_time_index = int(event['start_time'].strftime('%H')) - 9
    end_time_index = int(event['end_time'].strftime('%H')) - 9
    schedule[user_index, date_index, start_time_index:end_time_index] = 1

# Define the probability function
def calculate_probability(schedule):
    probabilities = []
    for user_index, user in enumerate(users):
        available_time = torch.sum(schedule[user_index] == 0)
        busy_time = torch.sum(schedule[user_index] == 1)
        probability = torch.exp(temperature * busy_time / available_time)
        probabilities.append(probability)
    total_probability = torch.prod(torch.tensor(probabilities))
    return total_probability

# Run the MCMC algorithm
for i in range(num_iterations):
    # Choose a random event and a new user and time slot
    event_index = random.randint(0, len(events)-1)
    event = events[event_index]
    new_user = random.choice(users)
    new_start_time = datetime.datetime.combine(event['date'], datetime.time(random.randint(9, 16), 0))
    new_end_time = new_start_time + datetime.timedelta(hours=random.randint(1, 3))
    new_start_time_index = int(new_start_time.strftime('%H')) - 9
    new_end_time_index = int(new_end_time.strftime('%H')) - 9
    
    # If the new user is the same as the old user, skip the move
    if new_user == event['user']:
        continue
    
    # Copy the schedule and make the move
    new_schedule = schedule.clone()
    user_index = users.index(event['user'])
    date_index = (event['date'] - start_date).days
    start_time_index = int(event['start_time'].strftime('%H')) - 9
    end_time_index = int(event['end_time'].strftime('%H')) - 9
    new_schedule[user_index, date_index, start_time_index:end_time_index] = 0
    new_user

    new_user_index = users.index(new_user)
    new_date_index = (event['date'] - start_date).days
    if (new_schedule[new_user_index, new_date_index, new_start_time_index:new_end_time_index] == 1).any():
        continue
    new_schedule[new_user_index, new_date_index, new_start_time_index:new_end_time_index] = 1

    # Calculate the acceptance probability
    old_probability = calculate_probability(schedule)
    new_probability = calculate_probability(new_schedule)
    acceptance_probability = min(1, new_probability / old_probability)

    # Accept or reject the move
    if random.random() < acceptance_probability:
        schedule = new_schedule

# Print to csv
with open('optimized_calendar_events.csv', mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['User', 'Event Type', 'Date', 'Start Time', 'End Time'])
    for event in events:
        user_index = users.index(event['user'])
        date_index = (event['date'] - start_date).days
        start_time_index = int(event['start_time'].strftime('%H')) - 9
        end_time_index = int(event['end_time'].strftime('%H')) - 9
        if schedule[user_index, date_index, start_time_index:end_time_index].sum() == 0:
            writer.writerow([event['user'], event['event_type'], event['date'], event['start_time'], event['end_time']])
            schedule[user_index, date_index, start_time_index:end_time_index] = 1