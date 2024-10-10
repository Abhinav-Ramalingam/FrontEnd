from flask import Flask, render_template, abort, request, jsonify
import bcrypt
import base64
import requests  # For HTTP requests to the logger
import json
import paho.mqtt.client as mqtt
from paho.mqtt.properties import Properties
from paho.mqtt.packettypes import PacketTypes
from flask_socketio import SocketIO, emit

app = Flask(__name__)
socketio = SocketIO(app)  # Initialize SocketIO

# MQTT Broker Configuration
BROKER_IP = '192.168.0.206'
BROKER_PORT = 1883
BROKER_USER = 'abhinavram2002'
BROKER_PASSWORD = '@209AoRQeFkeW'

# MQTT setup
client = mqtt.Client()
client.username_pw_set(BROKER_USER, BROKER_PASSWORD)

# Properties for MQTT
properties = Properties(PacketTypes.PUBLISH)

# Global variable for username
global_username = None

# Callback for handling incoming messages
def on_message(client, userdata, msg):
    payload = json.loads(msg.payload)
    # Store the received message in memory only if it's not from the current user
    if payload['username'] != global_username:
        print("Received message:", payload) 
        # Emit the message to all connected WebSocket clients
        socketio.emit('new_message', payload)  # Broadcast to all clients

# Callback for handling connection events
def on_connect(client, userdata, flags, reason_code):
    print("Connected with result code:", reason_code)

# Assign the callbacks to the client
client.on_connect = on_connect
client.on_message = on_message

# Connect to the MQTT broker
client.connect(BROKER_IP, BROKER_PORT, 60)
client.loop_start()  # Start the MQTT loop to process incoming messages

# Function to hash usernames using bcrypt and encode in Base64
def hash_username(username):
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(username.encode(), salt)
    return base64.urlsafe_b64encode(hashed).decode()  # Convert bytes to string

@app.route('/')
def intro():
    return render_template('intro.html', title='Intro Page')

@app.route('/chat/', methods=['GET', 'POST'])
def chat_main():
    global global_username  # Use global variable
    if request.method == 'POST':
        chat_code = request.form['chatCode']  # Get chat code from the form input
        global_username = request.form['username']  # Store the username in a global variable
        chat_code_with_topic = 'topic/' + chat_code  # Append "topic/" for the logger request
        
        # Make a request to the logger service to get chat messages
        logger_url = f"http://192.168.0.206:1337/getChat"  # Replace with your logger's IP and port
        response = requests.post(logger_url, json={"chat": chat_code_with_topic})

        if response.status_code == 200:
            messages = response.json()  # Get messages as a JSON object
            chat_name = chat_code_with_topic  # Set chat_name for display
            
            # Subscribe to the topic dynamically
            client.subscribe(chat_code_with_topic, qos=2)  # Subscribe to the topic here
            print("Subscribed to", chat_code_with_topic)

            # Pass the username to the chat.html template
            return render_template('chat.html', title=chat_name, chat_name=chat_name, chat_id=chat_code, messages=messages, chat_username=global_username)  
        else:
            abort(404)  # Handle errors appropriately

    return render_template('chat_main.html', title='Join a Chat')

@app.route('/send_message/', methods=['POST'])
def send_message():
    """Handle the AJAX request to send a message via MQTT."""
    data = request.json  # Get the JSON data from the request
    message = data.get('message')
    topic = data.get('topic')
    username = data.get('username')  # Default to 'abhinav' if not provided
    device_id = data.get('deviceID')

    # Format the payload
    payload = {
        "username": username,
        "deviceID": device_id,
        "message": message
    }
    # Publish the message to the MQTT topic
    client.publish(topic, json.dumps(payload), 2, properties=properties)

    return jsonify({"status": "Message sent", "payload": payload})

# Run the SocketIO server
if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=8000, debug=True)
