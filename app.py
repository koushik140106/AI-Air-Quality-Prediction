from flask import Flask, render_template, request
import pandas as pd
import os

# Try to load ML model safely
MODEL_AVAILABLE = False
model = None

try:
    import joblib
    if os.path.exists("pm25_model.pkl"):
        model = joblib.load("pm25_model.pkl")
        MODEL_AVAILABLE = True
except Exception:
    MODEL_AVAILABLE = False


app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def home():
    prediction = None
    quality = None
    mode = None

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

            # ✅ Use ML model if available
            if MODEL_AVAILABLE:
                prediction = float(model.predict(input_data)[0])
                mode = "ML Model"

            # ✅ Fallback logic (Render-safe)
            else:
                prediction = (
                    (pm10 * 0.4) +
                    (no * 0.2) +
                    (no2 * 0.2) +
                    (so2 * 0.1) +
                    (co * 10)
                )
                mode = "Rule-based AI (Demo)"

            # Air quality classification
            if prediction < 30:
                quality = "Good 😊"
            elif prediction < 60:
                quality = "Moderate 😐"
            else:
                quality = "Poor 😷"

        except Exception as e:
            prediction = None
            quality = None
            mode = None

    return render_template(
        "index.html",
        prediction=prediction,
        quality=quality,
        mode=mode
    )


if __name__ == "__main__":
    app.run()
