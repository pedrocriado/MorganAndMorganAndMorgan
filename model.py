import torch
import random

# Define the problem objective function
def objective_function(schedule):
    # Calculate the total time taken to complete all tasks in the schedule
    total_time = 0
    for task in schedule:
        total_time += task.duration
    return total_time

# Define the state space
def generate_random_schedule(num_tasks):
    schedule = []
    for i in range(num_tasks):
        task = {
            'name': f'Task {i+1}',
            'duration': random.randint(1, 8) # randomly generate task duration between 1 and 8 hours
        }
        schedule.append(task)
    return schedule

# Define the transition probability function
def swap_tasks(schedule):
    # randomly swap the order of two tasks in the schedule
    i, j = random.sample(range(len(schedule)), 2)
    schedule[i], schedule[j] = schedule[j], schedule[i]
    return schedule

# Define the acceptance probability function
def acceptance_probability(delta, temperature):
    return torch.exp(-delta / temperature)

# Set the temperature parameter
temperature = 1.0

# Initialize the current state
current_schedule = generate_random_schedule(num_tasks)

# Run the MCMC algorithm
for i in range(num_iterations):
    # Propose a new state
    new_schedule = swap_tasks(current_schedule)
    
    # Calculate the change in objective function value
    delta = objective_function(new_schedule) - objective_function(current_schedule)
    
    # Calculate the acceptance probability
    accept_prob = acceptance_probability(delta, temperature)
    
    # Decide whether to accept or reject the proposed state
    if accept_prob > random.uniform(0, 1):
        current_schedule = new_schedule
    
# Extract the optimal schedule
optimal_schedule = current_schedule
