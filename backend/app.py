from flask import Flask, render_template
from flask_socketio import SocketIO, send
import firebase_admin
from firebase_admin import credentials, firestore
import json

app = Flask(__name__)
socketio = SocketIO(app)

# Initialize Firebase Admin SDK
cred = credentials.Certificate("/backend/credentials(dontpush).json")
firebase_admin.initialize_app(cred)
db = firestore.client()

# Route for frontend to load the chat interface
@app.route('/')
def index():
    return render_template('index.html')

# Handle incoming messages from Socket.IO
@socketio.on('message')
def handle_message(msg):
    print(f"Received message: {msg}")

    # Save message to Firebase Firestore
    message_data = {
        "user": msg['user'],
        "text": msg['text'],
        "timestamp": msg['timestamp']
    }
    db.collection('messages').add(message_data)

    # Send message to all connected clients
    send(msg, broadcast=True)

if __name__ == '__main__':
    socketio.run(app, debug=True)
