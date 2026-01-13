import joblib
import pandas as pd

model = joblib.load("pm25_model.pkl")

# Create input as DataFrame with correct feature names
input_data = pd.DataFrame([{
    "PM10": 120,
    "NO": 20,
    "NO2": 30,
    "SO2": 10,
    "CO": 1.2
}])

prediction = model.predict(input_data)[0]

print("Predicted PM2.5 value:", prediction)

if prediction < 30:
    print("Air Quality: GOOD")
elif prediction < 60:
    print("Air Quality: MODERATE")
else:
    print("Air Quality: POOR")
