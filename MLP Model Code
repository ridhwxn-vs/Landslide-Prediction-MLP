import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import (confusion_matrix, accuracy_score, precision_score, recall_score, f1_score,roc_auc_score,classification_report)
from sklearn.preprocessing import StandardScaler
from keras.models import Sequential
from keras.layers import Dense
import matplotlib.pyplot as plt
from keras.optimizers import Adam

# Assuming 'data' is your DataFrame containing the dataset

# Drop features with moderate correlation to the target ('landslide')
features_to_drop = ['soil','rainfall']  # Drop features with moderate correlation
X = data.drop(columns=features_to_drop + ['landslide'])  # Drop target 'landslide' and the chosen features
y = data['landslide']  # Keep 'landslide' as the target

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Feature scaling (important for MLP)
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Build the MLP model
model = Sequential()
model.add(Dense(128, input_dim=X_train_scaled.shape[1], activation='relu'))  # First hidden layer
model.add(Dense(64, activation='relu'))  # Second hidden layer
model.add(Dense(1, activation='sigmoid'))  # Output layer (binary classification)

# Compile the model
model.compile(optimizer=Adam(), loss='binary_crossentropy', metrics=['accuracy'])

# Train the model
history = model.fit(X_train_scaled, y_train, epochs=50, batch_size=32, validation_data=(X_test_scaled, y_test))

# Predict on the test set
y_pred = (model.predict(X_test_scaled) > 0.5).astype(int)

# Evaluate the model
conf_matrix = confusion_matrix(y_test, y_pred)
accuracy = accuracy_score(y_test, y_pred)
precision = precision_score(y_test, y_pred, average='weighted')  # Use 'macro', 'micro', or 'binary' as needed
recall = recall_score(y_test, y_pred, average='weighted')  # Adjust average as per your use case
f1 = f1_score(y_test, y_pred, average='weighted')  # Adjust average if necessary
classification_rep = classification_report(y_test, y_pred)
roc_auc = roc_auc_score(y_test, y_pred, multi_class='ovr')  # For multi-class, use 'ovr' or 'ovo'


print(f"Accuracy: {accuracy:.4f}, Precision: {precision:.4f}, Recall: {recall:.4f}, F1 Score: {f1:.4f}")
print("\nConfusion Matrix:")
print(conf_matrix)
print("\nClassification Report:\n", classification_rep)
print("\nROC AUC Score:", roc_auc)
#model.save("landslide_model.keras")

plt.figure(figsize=(12, 5))
plt.subplot(1, 2, 1)
plt.plot(history.history['accuracy'], label='Train Accuracy')
plt.plot(history.history['val_accuracy'], label='Validation Accuracy')
plt.title('Model Accuracy')
plt.xlabel('Epochs')
plt.ylabel('Accuracy')
plt.legend()

# Plot training & validation loss values
plt.subplot(1, 2, 2)
plt.plot(history.history['loss'], label='Train Loss')
plt.plot(history.history['val_loss'], label='Validation Loss')
plt.title('Model Loss')
plt.xlabel('Epochs')
plt.ylabel('Loss')
plt.legend()

plt.show()

model.save("unoptimized_landslide_model.keras")
