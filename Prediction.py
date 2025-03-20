from keras.models import load_model
import pandas as pd
from sklearn.preprocessing import StandardScaler

# Load the saved model
model = load_model("model.keras")

# Load the dataset for prediction (ensure this CSV contains the correct features)
data_for_prediction = pd.read_csv("filename.csv")

print(data_for_prediction.head())


# Clean the dataset (drop system.index and .geo columns)
data_for_prediction_clean = data_for_prediction.drop(columns=['system:index', '.geo','rainfall','soil'])

# Display the cleaned dataset (you can check to verify the data)
print(data_for_prediction_clean.head())

# Initialize the scaler
scaler = StandardScaler()

# Scale only the relevant features (exclude .geo column)
data_for_prediction_scaled = scaler.fit_transform(data_for_prediction_clean)

# Make predictions (probabilities)
predictions = model.predict(data_for_prediction_scaled)

# Convert the predictions into a DataFrame for easy handling
predicted_probabilities = pd.DataFrame(predictions, columns=['landslide_probability'])

# Add the .geo and system.index (to map to spatial locations)
predicted_probabilities['system:index'] = data_for_prediction['system:index']
predicted_probabilities['.geo'] = data_for_prediction['.geo']  # Retain the .geo column

# Save the predictions to a CSV file
predicted_probabilities.to_csv("filename.csv", index=False)

