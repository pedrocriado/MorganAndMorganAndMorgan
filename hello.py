import pandas as pd
import torch
from torch.utils.data import DataLoader, TensorDataset
from sklearn.model_selection import train_test_split

# Load the data from the CSV file
data = pd.read_csv('calendar_data.csv')

# Convert the date-time columns to pandas datetime format
data['start_time'] = pd.to_datetime(data['start_time'])
data['end_time'] = pd.to_datetime(data['end_time'])

# Extract the features and labels from the data
features = data[['username', 'email', 'start_time', 'end_time']]
labels = data['event_title']

# Convert the categorical features to numerical features using one-hot encoding
features = pd.get_dummies(features, columns=['username', 'email'])

# Split the data into training and validation sets
train_features, val_features, train_labels, val_labels = train_test_split(features, labels, test_size=0.2)

# Convert the data to PyTorch tensors
train_features_tensor = torch.tensor(train_features.values, dtype=torch.float32)
val_features_tensor = torch.tensor(val_features.values, dtype=torch.float32)
train_labels_tensor = torch.tensor(train_labels.values, dtype=torch.long)
val_labels_tensor = torch.tensor(val_labels.values, dtype=torch.long)

# Create PyTorch data loaders
train_dataset = TensorDataset(train_features_tensor, train_labels_tensor)
train_loader = DataLoader(train_dataset, batch_size=32, shuffle=True)
val_dataset = TensorDataset(val_features_tensor, val_labels_tensor)
val_loader = DataLoader(val_dataset, batch_size=32)
