from flask import Flask, render_template

app = Flask(__name__)

# Sample data for chats
chats = [
    {"id": 1, "name": "Alice"},
    {"id": 2, "name": "Bob"},
    {"id": 3, "name": "Charlie"}
]

@app.route('/')
def intro():
    return render_template('intro.html', title='Intro Page')

@app.route('/chat')
def chat_list():
    return render_template('chat_list.html', title='Chat List', chats=chats)

@app.route('/chat/<int:chat_id>')
def chat(chat_id):
    chat_name = next((chat['name'] for chat in chats if chat['id'] == chat_id), "Chat not found")
    return render_template('chat.html', title=chat_name, chat_name=chat_name, chat_id=chat_id)

if __name__ == '__main__':
    app.run(port=5000, debug=True)
