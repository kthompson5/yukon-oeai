from flask import Flask, render_template, jsonify, request
import requests

app = Flask(__name__)

# Coordinates for Yukon Bible Church
LAT = 35.5062
LON = -97.7668

# ----- OEAI Calculation with Age Adjustment and Updated Risk Labels -----
def calculate_oeai(temp_f, humidity, wind_speed, heat_index, cloud_cover, age_group):
    # Base score calculation
    score = (
        (100 - abs(75 - temp_f)) * 0.3 +
        (100 - humidity) * 0.2 +
        (20 - wind_speed) * 5 * 0.15 +
        (100 - abs(80 - heat_index)) * 0.3 +
        (100 - cloud_cover) * 0.05
    )

    # Age group adjustment
    age_modifiers = {
        "4-6": -15,
        "7-9": -10,
        "10-12": -5,
        "13+": 0
    }
    adjustment = age_modifiers.get(age_group, 0)
    score += adjustment

    # Clamp score
    score = max(0, min(100, score))

    # Comfort message & risk level
    if score >= 80:
        message = "Perfect for play! Mild temps and light breeze."
        risk = "GOOD TO GO"
    elif score >= 60:
        message = "Good weather. Hydrate and watch for sunburn."
        risk = "GOOD TO GO"
    elif score >= 40:
        message = "Warm. Take shade breaks and hydrate regularly."
        risk = "CAUTION — TAKE PRECAUTIONS"
    else:
        message = "Too hot for safe play. Encourage frequent breaks and shade."
        risk = "HIGH STRESS — MONITOR CLOSELY"

    return round(score), message, risk

# ----- Hour-Specific Weather Forecast Route -----
@app.route("/api/game-forecast")
def get_game_forecast():
    age_group = request.args.get("age_group", "13+")
    hour = int(request.args.get("hour", 10))  # default 10 AM

    url = (
        f"https://api.open-meteo.com/v1/forecast"
        f"?latitude={LAT}&longitude={LON}"
        f"&hourly=temperature_2m,relativehumidity_2m,windspeed_10m,cloudcover"
        f"&current_weather=true"
        f"&timezone=America/Chicago"
    )
    res = requests.get(url)
    data = res.json()

    hourly = data.get("hourly", {})

    # Pull the weather for the requested hour
    try:
        temp_c = hourly.get("temperature_2m", [])[hour]
        humidity = hourly.get("relativehumidity_2m", [])[hour]
        wind_speed = hourly.get("windspeed_10m", [])[hour]
        cloud_cover = hourly.get("cloudcover", [])[hour]
    except (IndexError, TypeError):
        return jsonify({"error": "Invalid hour or missing forecast data."}), 400

    temp_f = temp_c * 9/5 + 32
    heat_index = temp_f  # placeholder

    score, message, risk = calculate_oeai(temp_f, humidity, wind_speed, heat_index, cloud_cover, age_group)

    return jsonify({
        "hour": hour,
        "temp_f": round(temp_f, 1),
        "humidity": humidity,
        "wind_speed": wind_speed,
        "cloud_cover": cloud_cover,
        "oeai": score,
        "comfort_message": message,
        "risk_level": risk
    })

# ----- Home Route -----
@app.route("/")
def home():
    return render_template("index.html")

# ----- Game Day Forecast Page -----
@app.route("/gameday")
def gameday():
    return render_template("gameday.html")

if __name__ == "__main__":
    app.run(debug=True)