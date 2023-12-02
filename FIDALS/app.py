from flask import Flask, redirect, url_for,render_template
from flask_socketio import SocketIO
import random

app = Flask(__name__)
socketio = SocketIO(app)

# Simulated temperature data for demonstration purposes
def get_temperature():
    return random.uniform(70, 90)

@app.route('/')
def index():
    return render_template('index.html')

# WebSocket event to send temperature data to the client
@socketio.on('temperature_data')
def send_temperature_data():
    print(get_temperature)
    temperature = get_temperature()
    socketio.emit('update_temperature', {'temperature': temperature})

if __name__ == '__main__':
    app.run(debug = True, port=5050)
