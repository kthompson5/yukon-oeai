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
        message =