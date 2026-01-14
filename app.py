from flask import Flask, render_template, request
import pandas as pd

app = Flask(__name__)

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

            # 🔹 Lightweight prediction logic (demo-safe)
            prediction = (pm10 * 0.4) + (no * 0.2) + (no2 * 0.2) + (so2 * 0.1) + (co * 10)

            if prediction < 30:
                quality = "Good 😊"
            elif prediction < 60:
                quality = "Moderate 😐"
            else:
                quality = "Poor 😷"

        except Exception:
            prediction = None
            quality = None

    return render_template(
        "index.html",
        prediction=prediction,
        quality=quality
    )

if __name__ == "__main__":
    app.run()
