from flask import Flask, render_template, request
import joblib
import pandas as pd
import os
import traceback

# -------------------------------
# Create Flask application
# -------------------------------
app = Flask(__name__, static_folder="static")

print("Flask app file loaded")

# -------------------------------
# Load ML model safely
# -------------------------------
try:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    MODEL_PATH = os.path.join(BASE_DIR, "pm25_model.pkl")
    model = joblib.load(MODEL_PATH)
    print("Model loaded successfully")
except Exception as e:
    print("ERROR loading model:")
    traceback.print_exc()
    model = None

# -------------------------------
# Home route
# -------------------------------
@app.route("/", methods=["GET", "POST"])
def home():
    prediction = None
    quality = None
    error = None

    if request.method == "POST":
        try:
            print("Form received:", request.form)

            pm10 = float(request.form.get("pm10"))
            no = float(request.form.get("no"))
            no2 = float(request.form.get("no2"))
            so2 = float(request.form.get("so2"))
            co = float(request.form.get("co"))

            input_df = pd.DataFrame([{
                "PM10": pm10,
                "NO": no,
                "NO2": no2,
                "SO2": so2,
                "CO": co
            }])

            print("Input DataFrame:")
            print(input_df)

            if model is None:
                raise Exception("Model not loaded")

            prediction = float(model.predict(input_df)[0])

            if prediction < 30:
                quality = "Good"
            elif prediction < 60:
                quality = "Moderate"
            else:
                quality = "Poor"

        except Exception as e:
            print("ERROR during prediction:")
            traceback.print_exc()
            error = str(e)

    return render_template(
        "index.html",
        prediction=prediction,
        quality=quality,
        error=error
    )

# -------------------------------
# Run server (NO reloader)
# -------------------------------
if __name__ == "__main__":
    print("Starting Flask server...")
    app.run(
        host="0.0.0.0",
        port=10000,
        debug=True,
        use_reloader=False
    )
