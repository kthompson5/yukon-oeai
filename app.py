from flask import Flask, render_template, jsonify
import requests

app = Flask(__name__)

# Coordinates for Yukon Bible Church
LAT = 35.5062
LON = -97.7668

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
    url = (
        f"https://api.open-meteo.com/v1/forecast"
        f"?latitude={LAT}&longitude={LON}"
        f"&hourly=temperature_2m,relativehumidity_2m,windspeed_10m,cloudcover"
        f"&current_weather=true"
    )
    res = requests.get(url)
    data = res.json()

    current = data.get("current_weather", {})
    hourly = data.get("hourly", {})

    temp_c = current.get("temperature", 0)
    temp_f = temp_c * 9/5 + 32
    wind_speed = current.get("windspeed", 0)
    cloud_cover = hourly.get("cloudcover", [0])[0] if hourly.get("cloudcover") else 0
    humidity = hourly.get("relativehumidity_2m", [0])[0] if hourly.get("relativehumidity_2m") else 50

    heat_index = temp_f  # Placeholder; actual heat index can be calculated later

    score, message = calculate_oeai(temp_f, humidity, wind_speed, heat_index, cloud_cover)

    return jsonify({
        "temp_f": round(temp_f, 1),
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
