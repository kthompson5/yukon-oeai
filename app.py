from flask import Flask, render_template, jsonify
import requests
import os

app = Flask(__name__)

# Coordinates for Yukon Bible Church\NLAT = 35.5062
LON = -97.7668

# OpenWeatherMap API Key (use your own key from Render environment variables)
API_KEY = os.getenv("OWM_API_KEY")

# ----- OEAI Calculation -----
def calculate_oeai(temp_f, humidity, wind_speed, heat_index, cloud_cover):
    # Example weighted formula
    score = (
        (100 - abs(75 - temp_f)) * 0.3 +
        (100 - humidity) * 0.2 +
        (20 - wind_speed) * 5 * 0.15 +
        (100 - abs(80 - heat_index)) * 0.3 +
        (100 - cloud_cover) * 0.05
    )
    score = max(0, min(100, score))

    if score >= 80:
        message = "Perfect for play! Mild temps and light breeze."
    elif score >= 60:
        message = "Good weather. Hydrate and watch for sunburn."
    elif score >= 40:
        message = "Warm. Take shade breaks and hydrate regularly."
    else:
        message = "Too hot for safe play. Limit outdoor activity."

    return round(score), message

# ----- Weather Route -----
@app.route("/api/weather")
def get_weather():
    url = f"https://api.openweathermap.org/data/3.0/onecall?lat={LAT}&lon={LON}&units=imperial&appid={API_KEY}"
    res = requests.get(url)
    data = res.json()

    current = data.get("current", {})

    temp_f = current.get("temp")
    humidity = current.get("humidity")
    wind_speed = current.get("wind_speed")
    heat_index = temp_f  # Placeholder; OpenWeatherMap doesn't give heat index directly
    cloud_cover = current.get("clouds")

    score, message = calculate_oeai(temp_f, humidity, wind_speed, heat_index, cloud_cover)

    return jsonify({
        "temp_f": temp_f,
        "humidity": humidity,
        "wind_speed": wind_speed,
        "cloud_cover": cloud_cover,
        "oeai": score,
        "comfort_message": message
    })

# ----- Frontend Route -----
@app.route("/")
def home():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
