from flask import Flask, render_template, abort, request, jsonify
import bcrypt
import base64
import requests  # For HTTP requests to the logger
import json
import paho.mqtt.client as mqtt
from paho.mqtt.properties import Properties
from paho.mqtt.packettypes import PacketTypes
from datetime import datetime

app = Flask(__name__)

# MQTT Broker Configuration
BROKER_IP = '192.168.0.206'
BROKER_PORT = 1883
BROKER_USER = 'abhinavram2002'
BROKER_PASSWORD = '@209AoRQeFkeW'
DEVICE_ID = 'testID'

# MQTT setup
client = mqtt.Client()
client.username_pw_set(BROKER_USER, BROKER_PASSWORD)

# Properties for MQTT
properties = Properties(PacketTypes.PUBLISH)
properties.MessageExpiryInterval = 30  # in seconds

# Callback for handling incoming messages
def on_message(client, userdata, msg):
    payload = json.loads(msg.payload)
    print("Received message:", payload)  # Log the received message for now

    # You can add logic here to update your chat interface if necessary

# Callback for handling connection events
def on_connect(client, userdata, flags, reason_code):
    print("Connected with result code:", reason_code)
    # Subscribe to a default topic or take dynamic action based on application logic

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
    if request.method == 'POST':
        chat_code = request.form['chatCode']  # Get chat code from the form input
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
            return render_template('chat.html', title=chat_name, chat_name=chat_name, chat_id=chat_code, messages=messages)  
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
    device_id = data.get('deviceID', DEVICE_ID)

    # Format the payload
    payload = {
        "username": username,
        "deviceID": device_id,
        "message": message
    }
    print('payload: ',payload)
    # Publish the message to the MQTT topic
    client.publish(topic, json.dumps(payload), 2, properties=properties)

    return jsonify({"status": "Message sent", "payload": payload})

# Custom error handler for 404 errors
@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
