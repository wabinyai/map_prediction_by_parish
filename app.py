# Import necessary libraries
import os
from flask import Flask, jsonify, render_template, request
import requests
import geojson
from dotenv import load_dotenv

# Create a Flask app
app = Flask(__name__)
load_dotenv()

API_URL = "https://platform.airqo.net/api/v2/predict/search"

# Function to fetch PM2.5 values from the API
def fetch_pm2_5_data(latitude, longitude, token):
    # Prepare the API URL with query parameters
    api_params = {
        "latitude": latitude,
        "longitude": longitude,
        "token": token,
    }
    try:
        response = requests.get(API_URL, params=api_params)
        response.raise_for_status()  # Check for any request errors
        pm2_5_data = response.json()  # Parse the JSON response
        return pm2_5_data
    except requests.exceptions.RequestException as e:
        print(f"Error fetching PM2.5 data from the API: {e}")
        return None

# Route to access geo data from the API
@app.route("/geo")
def connect_to_api():
    try:
        # Get user's latitude and longitude from query parameters
        user_latitude = float(request.args.get("latitude"))
        user_longitude = float(request.args.get("longitude"))

        # Fetch PM2.5 data from the API
        pm2_5_data = fetch_pm2_5_data(user_latitude, user_longitude, os.environ.get("AIRQO_API_TOKEN"))

        if pm2_5_data:
            # Process the retrieved data and create a GeoJSON response
            features = [
                geojson.Feature(
                    id=str(index),
                    geometry=geojson.Point((user_longitude, user_latitude)),
                    properties={"pm2_5": pm2_5_value}
                ) for index, pm2_5_value in enumerate(pm2_5_data)
            ]

            feature_collection = geojson.FeatureCollection(features)
            return jsonify(feature_collection)
        else:
            return "Failed to fetch PM2.5 data from the API.", 500
    except Exception as e:
        print(f"Error: {e}")
        return "An error occurred while processing the request.", 500



# Route to display the map
@app.route("/")
def home():
    return render_template("map.html")


# Run the Flask app on port 5000
if __name__ == "__main__":
    app.run(debug=True, port=5000)
