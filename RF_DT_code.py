from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score, classification_report, confusion_matrix
import pandas as pd
import numpy as np

# Re-add 'builtUp' and remove 'rainfall' and other correlated features
features_to_drop = ['soil','rainfall']  # Keep 'builtUp' and remove 'rainfall' along with others
X = data.drop(columns=features_to_drop + ['landslide'])  # Drop target 'landslide'
y = data['landslide']

# Shuffle the data (optional but can help generalize)
X, y = X.sample(frac=1, random_state=42).reset_index(drop=True), y.sample(frac=1, random_state=42).reset_index(drop=True)

# Split into training and test sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Regularize models
decision_tree = DecisionTreeClassifier(max_depth=5, min_samples_split=10, random_state=42)
random_forest = RandomForestClassifier(n_estimators=100, max_depth=5, min_samples_split=10, random_state=42)

# Fit the models on the full training data
decision_tree.fit(X_train, y_train)
random_forest.fit(X_train, y_train)

# Make predictions on the test set
y_pred_dt = decision_tree.predict(X_test)
y_pred_rf = random_forest.predict(X_test)

# Predict probabilities for ROC Curve (for AUC)
y_pred_proba_dt = decision_tree.predict_proba(X_test)[:, 1]
y_pred_proba_rf = random_forest.predict_proba(X_test)[:, 1]

# Compute metrics for Decision Tree
accuracy_dt = accuracy_score(y_test, y_pred_dt)
precision_dt = precision_score(y_test, y_pred_dt, pos_label=1)
recall_dt = recall_score(y_test, y_pred_dt, pos_label=1)
f1_dt = f1_score(y_test, y_pred_dt, pos_label=1)
roc_auc_dt = roc_auc_score(y_test, y_pred_proba_dt)

# Compute metrics for Random Forest
accuracy_rf = accuracy_score(y_test, y_pred_rf)
precision_rf = precision_score(y_test, y_pred_rf, pos_label=1)
recall_rf = recall_score(y_test, y_pred_rf, pos_label=1)
f1_rf = f1_score(y_test, y_pred_rf, pos_label=1)
roc_auc_rf = roc_auc_score(y_test, y_pred_proba_rf)

# Print evaluation metrics
print("\nEvaluation Metrics for Decision Tree:")
print(f"Accuracy: {accuracy_dt:.4f}, Precision: {precision_dt:.4f}, Recall: {recall_dt:.4f}, F1 Score: {f1_dt:.4f}, ROC AUC: {roc_auc_dt:.4f}")
print("\nEvaluation Metrics for Random Forest:")
print(f"Accuracy: {accuracy_rf:.4f}, Precision: {precision_rf:.4f}, Recall: {recall_rf:.4f}, F1 Score: {f1_rf:.4f}, ROC AUC: {roc_auc_rf:.4f}")

# Print confusion matrix and classification report for both models
print("\nConfusion Matrix for Decision Tree:")
print(confusion_matrix(y_test, y_pred_dt))
print(f"\nClassification Report for Decision Tree:")
print(classification_report(y_test, y_pred_dt))

print("\nConfusion Matrix for Random Forest:")
print(confusion_matrix(y_test, y_pred_rf))
print(f"\nClassification Report for Random Forest:")
print(classification_report(y_test, y_pred_rf))


