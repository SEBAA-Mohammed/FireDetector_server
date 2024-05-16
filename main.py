import socketio
from flask_cors import CORS
from flask import Flask, request, send_file

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Initialize Socket.IO server with eventlet
sio = socketio.Server(cors_allowed_origins='http://localhost:3000', async_mode='eventlet')

# Function to send a message to the client
def send_message_to_client(message):
    sio.emit('coordinates', message)  # Send message to all clients

# Define endpoint for receiving messages from the user
@app.route('/send-message', methods=['POST'])
def send_message():
    message = request.json.get('coordinates')
    send_message_to_client(message)  # Send message to client(s)
    return 'Message sent to clients'

# end point for images
@app.route('/image', methods=['POST'])
def receive_image():
    if 'image' not in request.files:
        return 'No image uploaded', 400

    image_file = request.files['image']
    image_bytes = image_file.read()  # Read the image bytes

    # Send the image bytes to the client
    sio.emit('image', image_bytes)

    return 'Image received and sent to clients'

# Attach Socket.IO server to Flask app
app.wsgi_app = socketio.WSGIApp(sio, app.wsgi_app)

if __name__ == '__main__':
    # Run the server using eventlet
    import eventlet
    eventlet.wsgi.server(eventlet.listen(('localhost', 5001)), app)
