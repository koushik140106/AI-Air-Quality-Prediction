from flask import Flask, render_template, request
import joblib
import pandas as pd

app = Flask(__name__)

# Load trained model
model = joblib.load("pm25_model.pkl")

@app.route("/", methods=["GET", "POST"])
def home():
    prediction = None
    quality = None

    if request.method == "POST":
        try:
            pm10 = float(request.form.get("pm10"))
            no = float(request.form.get("no"))
            no2 = float(request.form.get("no2"))
            so2 = float(request.form.get("so2"))
            co = float(request.form.get("co"))

            input_data = pd.DataFrame([{
                "PM10": pm10,
                "NO": no,
                "NO2": no2,
                "SO2": so2,
                "CO": co
            }])

            prediction = float(model.predict(input_data)[0])

            if prediction < 30:
                quality = "Good 😊"
            elif prediction < 60:
                quality = "Moderate 😐"
            else:
                quality = "Poor 😷"

        except Exception as e:
            prediction = None
            quality = "Error"

    # 🔴 IMPORTANT: ALWAYS return prediction & quality
    return render_template(
        "index.html",
        prediction=prediction,
        quality=quality
    )

if __name__ == "__main__":
    app.run(debug=True)
