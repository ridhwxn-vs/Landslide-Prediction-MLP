import pandas as pd

# Load the CSV file into a DataFrame
data = pd.read_csv('filename.csv') 

# Check if the '.geo' column exists and drop it if present
if '.geo' in data.columns:
    data = data.drop(columns=['.geo'], axis=1)



# Drop the index column if not needed
if 'system:index' in data.columns:
    data = data.drop(columns=['system:index'])

# Check for missing values
print("Missing values in each column:\n", data.isnull().sum())

# Separate features and labels
X = data.drop('landslide', axis=1)  # Features
y = data['landslide']  # Target variable

# Display the shapes of features and labels
print("Shape of Features (X):", X.shape)
print("Shape of Target (y):", y.shape)

