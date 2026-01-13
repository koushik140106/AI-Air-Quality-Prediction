import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, r2_score
import joblib

# Load cleaned data
df = pd.read_csv("cleaned_air_quality.csv")

print("Initial shape:", df.shape)

# Ensure all required columns exist
required_cols = ["PM25", "PM10", "NO", "NO2", "SO2", "CO"]
df = df[required_cols]

# FINAL NaN HANDLING (CRITICAL STEP)
df = df.dropna()

print("Shape after dropping NaNs:", df.shape)

# Features and target
X = df.drop("PM25", axis=1)
y = df["PM25"]

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Train model
model = LinearRegression()
model.fit(X_train, y_train)

# Evaluate
y_pred = model.predict(X_test)
mae = mean_absolute_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

# Save model
joblib.dump(model, "pm25_model.pkl")

print("✅ Model trained successfully")
print("Mean Absolute Error:", mae)
print("R2 Score:", r2)
