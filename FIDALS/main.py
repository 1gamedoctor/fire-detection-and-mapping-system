from flask import Flask, render_template
from flask_socketio import SocketIO
import requests
import json

app = Flask(__name__)
socketio = SocketIO(app)

# Replace 'YOUR_NASA_API_KEY' with your actual NASA API key
NASA_API_KEY = 'QJk4dLga6ufkkCmo754YYGf1SILx0XxMJIyxNWvs'
NASA_WORLDVIEW_URL = 'https://worldview.earthdata.nasa.gov'

@app.route('/')
def index():
    return render_template('thermal.html')

# WebSocket event to send satellite thermal image URL to the client
@socketio.on('get_satellite_image')
def get_satellite_image(bbox):
    image_url = fetch_satellite_image(bbox)
    socketio.emit('update_satellite_image', {'image_url': image_url})

def fetch_satellite_image(bbox):
    try:
        response = requests.get(
            f'{NASA_WORLDVIEW_URL}/api/v1/snapshot?REQUEST=GetSnapshot&LAYERS=MODIS_Terra_Thermal_Anomalies_24h&BBOX={bbox}&CRS=EPSG:4326&FORMAT=image/jpeg&WIDTH=1024&HEIGHT=512&TIME=2020-01-01&API_KEY={NASA_API_KEY}'
        )

        if response.status_code == 200:
            return response.url

    except Exception as e:
        print(f"Error fetching satellite image: {str(e)}")
    
    return None

if __name__ == '__main__':
    socketio.run(app, debug=True, port=5050)
