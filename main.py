from flask import Flask, render_template, abort
import bcrypt
import base64

app = Flask(__name__)

# Function to hash usernames using bcrypt and encode in Base64
def hash_username(username):
    # Generate a salt and hash the username
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(username.encode(), salt)
    # Encode the hashed bytes to a Base64 string
    return base64.urlsafe_b64encode(hashed).decode()  # decode to convert bytes to string

# Sample data for chats with hashed usernames
chats = [
    {"id": hash_username("alice"), "name": "Alice"},
    {"id": hash_username("bob"), "name": "Bob"},
    {"id": hash_username("charlie"), "name": "Charlie"}
]

@app.route('/')
def intro():
    return render_template('intro.html', title='Intro Page')

@app.route('/chat/')
def chat_list():
    return render_template('chat_list.html', title='Chat List', chats=chats)

@app.route('/chat/<chat_id>/')
def chat(chat_id):
    # Check if the chat ID exists in the hashed chat list
    chat = next((chat for chat in chats if chat['id'] == chat_id), None)

    if chat is None:
        abort(404)  # If chat not found, raise a 404 error

    chat_name = chat['name']
    return render_template('chat.html', title=chat_name, chat_name=chat_name, chat_id=chat_id)

# Custom error handler for 404 errors
@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404

if __name__ == '__main__':
    app.run(port=5000, debug=True)
