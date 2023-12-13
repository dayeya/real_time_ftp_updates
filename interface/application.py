from flask import Flask, render_template
from flask_socketio import SocketIO
import json

app = Flask(__name__)
socketio = SocketIO(app)

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('connect')
def handle_connect():
    print('Proxy connected')

@socketio.on('disconnect')
def handle_disconnect():
    print('Proxy disconnected')

@socketio.on('update_data')
def handle_update_data(data):
    try:
        # Attempt to parse the received data as JSON
        data = json.loads(data)
        # Process the data received from the proxy
        # You can implement your WAF logic here
        print('Received data from proxy:', data)

        # Emit an update to the connected clients
        socketio.emit('update_website', data)
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")

if __name__ == '__main__':
    socketio.run(app, 
                 host='127.0.0.1',
                 port=60000,
                 debug=True)