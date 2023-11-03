# Import necessary libraries
import os
from flask import Flask, jsonify, render_template, request
import requests
from dotenv import load_dotenv

# Create a Flask app
app = Flask(__name__)
load_dotenv()

# Define the API URL for fetching PM2.5 data
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
        # Send a GET request to the API with the query parameters
        response = requests.get(API_URL, params=api_params)
        response.raise_for_status()  # Check for any request errors
        pm2_5_data = response.json()["data"]["pm2_5"]  # Extract PM2.5 value from the JSON response
        return pm2_5_data
    except requests.exceptions.RequestException as e:
        print(f"Error fetching PM2.5 data from the API: {e}")
        return None


# Route to access PM2.5 data from the API
@app.route("/geo")
def connect_to_api():
    try:
        # Get user's latitude and longitude from query parameters
        user_latitude = float(request.args.get("latitude"))
        user_longitude = float(request.args.get("longitude"))
        print("User Latitude:", user_latitude)
        print("User Longitude:", user_longitude)

        # Fetch PM2.5 data from the API using the provided coordinates and API token
        pm2_5_data = fetch_pm2_5_data(user_latitude, user_longitude, os.environ.get("AIRQO_API_TOKEN"))
        print("PM2.5 Data:", pm2_5_data)

        if pm2_5_data is not None:
            # Create a JSON object with the PM2.5 value
            pm2_5_json = {"pm2_5": pm2_5_data}
            print("PM2.5 JSON:", pm2_5_json)
            return jsonify(pm2_5_json)
        else:
            error_message = "Failed to fetch PM2.5 data from the API."
            print(error_message)
            return error_message, 500
    except Exception as e:
        error_message = "An error occurred while processing the request."
        print("Error:", e)
        print(error_message)
        return error_message, 500


# Route to display the map
@app.route("/")
def home():
    return render_template("map.html")

# Run the Flask app on port 5000 if executed as the main script
if __name__ == "__main__":
    app.run(debug=True, port=5000)
