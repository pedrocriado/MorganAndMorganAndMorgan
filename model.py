import torch
import torch.nn as nn
import torch.optim as optim

import csv
import datetime

# Define users
users = ['user' + str(i) for i in range(1, 101)]

# Define event types
event_types = ['Meeting', 'Lunch', 'Presentation', 'Training', 'Appointment']

# Define start and end dates
start_date = datetime.date(2023, 5, 1)
end_date = datetime.date(2023, 5, 31)

# Load data from CSV file
events = []
with open('calendar_events.csv', mode='r') as file:
    reader = csv.reader(file)
    next(reader) # Skip header row
    for row in reader:
        user, event_type, date, start_time, end_time = row
        events.append([users.index(user), event_types.index(event_type), (datetime.datetime.strptime(date, '%Y-%m-%d').toordinal() - start_date.toordinal()), (datetime.datetime.strptime(start_time, '%H:%M:%S').hour), (datetime.datetime.strptime(end_time, '%H:%M:%S').hour)])

# Convert data to PyTorch tensors
events = torch.tensor(events, dtype=torch.float32)

# Split data into training and validation sets
train_data = events[:400]
val_data = events[400:]

# Define PyTorch model
class EventDurationModel(nn.Module):
    def __init__(self):
        super(EventDurationModel, self).__init__()
        self.fc1 = nn.Linear(4, 16)
        self.fc2 = nn.Linear(16, 1)

    def forward(self, x):
        x = torch.relu(self.fc1(x))
        x = self.fc2(x)
        return x

# Define loss function and optimizer
criterion = nn.MSELoss()
optimizer = optim.Adam(EventDurationModel().parameters(), lr=0.01)

# Train PyTorch model
model = EventDurationModel()
num_epochs = 100
batch_size = 32
for epoch in range(num_epochs):
    running_loss = 0.0
    for i in range(0, len(train_data), batch_size):
        batch = train_data[i:i+batch_size]
        optimizer.zero_grad()
        outputs = model(batch[:, 0:4])
        loss = criterion(outputs, batch[:, 4].unsqueeze(1))
        loss.backward()
        optimizer.step()
        running_loss += loss.item()
    print('Epoch [%d/%d], Loss: %.4f' % (epoch+1, num_epochs, running_loss/len(train_data)))

# Evaluate PyTorch model on validation set
with torch.no_grad():
    val_outputs = model(val_data[:, 0:4])
    val_loss = criterion(val_outputs, val_data[:, 4].unsqueeze(1))
    print('Validation Loss: %.4f' % val_loss.item())
