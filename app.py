from flask import Flask, render_template, request
from configure import load_config
import requests

app = Flask(__name__)
config = load_config()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/map', methods=['POST'])
def map():
    # Get latitude and longitude from the form
    latitude = request.form['latitude']
    longitude = request.form['longitude']
    token = config['TOKEN']  # Get the token from the config

    # Construct the API URL with dynamic latitude and longitude
    dynamic_url = f"{config['PREDICT_URL']}latitude={latitude}&longitude={longitude}$token={token}"

    # Include the token in the request headers
    headers = {
        'Authorization': f'Bearer {token}'
    }

    # Make a request to the AirQo API with the token
    response = requests.get(dynamic_url, headers=headers)

    if response.status_code == 200:
        data = response.json().get("data")
        if data:
            district = data.get("district")
            parish = data.get("parish")
            pm25 = data.get("pm2_5")
            timestamp = data.get("timestamp")
        else:
            district, parish, pm25, timestamp = None, None, None, None
    else:
        district, parish, pm25, timestamp = None, None, None, None

    return render_template('map.html', district=district, parish=parish, pm25=pm25, timestamp=timestamp)

if __name__ == '__main__':
    app.run(debug=True)
