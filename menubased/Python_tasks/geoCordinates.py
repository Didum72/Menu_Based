from flask import Flask, render_template, request, jsonify
from geopy.geocoders import Nominatim

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('geoCordinates.html')

@app.route('/get_geo_coordinates', methods=['POST'])
def get_geo_coordinates():
    address = request.form.get('address')

    geolocator = Nominatim(user_agent="geoapi")
    location = geolocator.geocode(address)

    if location:
        coordinates = {
            'latitude': location.latitude,
            'longitude': location.longitude,
            'address': location.address
        }
    else:
        coordinates = {'error': 'Location not found'}

    return jsonify(coordinates)

if __name__ == '__main__':
    app.run(debug=True)
