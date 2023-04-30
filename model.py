import numpy as np
from collections import defaultdict

# Define the schedule as a sequence of time slots
n_time_slots = 24  # 24 slots of 30 minutes each

# Define the possible events that can occur during each time slot
events = ["Meeting", "Phone call", "Break"]

# Define the constraints that must be satisfied by the schedule
constraints = {
    "Availability": defaultdict(lambda: np.ones(n_time_slots)),  # Each party is available for all time slots
    "Duration": {"Meeting": 2, "Phone call": 1, "Break": 1},  # Each event has a fixed duration
    "Minimum time between events": {"Meeting": 2, "Phone call": 1, "Break": 1}  # Minimum time between events of the same type
}

# Define the preferences of the parties
preferences = {
    "Party A": {"Meeting": 5, "Phone call": 3, "Break": 2},  # Party A prefers meetings over phone calls and breaks
    "Party B": {"Meeting": 3, "Phone call": 4, "Break": 1},  # Party B prefers phone calls over meetings and breaks
    "Party C": {"Meeting": 1, "Phone call": 1, "Break": 5}   # Party C prefers breaks over meetings and phone calls
}

# Define the scoring function that assigns a score to each possible schedule
def score(schedule):
    conflicts = 0
    total_duration = 0
    for party, events in schedule.items():
        event_types = defaultdict(int)
        last_event_time = -1
        for event, time_slot in events:
            # Check availability constraint
            if not constraints["Availability"][party][time_slot]:
                conflicts += 1
            # Check minimum time between events constraint
            if last_event_time >= 0 and event_types[event] > 0 and time_slot - last_event_time < constraints["Minimum time between events"][event]:
                conflicts += 1
            # Update event types and last event time
            event_types[event] += 1
            last_event_time = time_slot
            # Update total duration
            total_duration += constraints["Duration"][event]
        # Apply party preferences
        party_score = sum(preferences[party][event] * event_types[event] for event in event_types)
        conflicts += party_score
    return -conflicts, -total_duration  # We maximize the negative of the score

# Define the proposal distribution that generates new schedules
def proposal(schedule):
    new_schedule = defaultdict(list)
    for party, events in schedule.items():
        for event, time_slot in events:
            new_time_slot = np.random.randint(n_time_slots)  # Randomly generate a new time slot
            new_schedule[party].append((event, new_time_slot))
    return new_schedule

# Define the Metropolis-Hastings algorithm
def metropolis_hastings(initial_schedule, n_iterations, proposal_sd):
    current_schedule = initial_schedule
    for i in range(n_iterations):
        proposal_schedule = proposal(current_schedule)  # Generate a proposal schedule
        acceptance_prob = min(1, np.exp(sum(score(proposal_schedule)) - sum(score(current_schedule))))  # Compute acceptance probability
        if np.random.uniform() < acceptance_prob:  # Accept or reject the proposal
            current_schedule = proposal_schedule
    return current_schedule

# Generate an initial schedule that satisfies the constraints
initial_schedule = {
"Party A": [("Meeting", 0), ("Break", 4), ("Meeting", 8)],
"Party B": [("Phone call", 2), ("Meeting", 6), ("Break", 10)],
"Party C": [("Break", 1), ("Meeting", 5), ("Break", 9)]
}

final_schedule = metropolis_hastings(initial_schedule, n_iterations=1000, proposal_sd=1)

print("Final schedule:")
for party, events in final_schedule.items():
    print(f"{party}:")
for event, time_slot in events:
    print(f" {event} at {time_slot}")

score_1, score_2 = score(final_schedule)
print(f"Final score: {-score_1}, {-score_2}")