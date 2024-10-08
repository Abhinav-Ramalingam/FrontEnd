from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def intro():
    return render_template('intro.html', title='Intro Page')

@app.route('/chat')
def chat():
    return render_template('chat.html', title='Chat Page')

if __name__ == '__main__':
    app.run(port=5000, debug=True)
