
from app import app, db, socketio
from user import *
from message import *
from game.MultPlayer import *
from notif import *
from friend import *
from game.playground import *
from game.AIScript import *
with app.app_context():
    # db.drop_all()
    db.create_all()
from game.TicTacToe import TicTacToe
from game.Maze import Maze
from game.HighLow import HighLow


@app.route('/', methods=['GET', 'POST'])
def hello_world():
    if request.method == 'POST':
        data = request.form.get('data')  # Replace 'data' with your form field name
        return f'Hello, World! (Received POST data: {data})'
    else:
        return 'Hello, World!'


@app.route('/pyexec', methods=['POST'])
def sendcode():
    code = request.get_json()
    local_scope = {}
    exec(code["code"], local_scope)
    return local_scope["choose_move"]()


if __name__ == '__main__':
    socketio.run(app, debug=True, host="0.0.0.0", allow_unsafe_werkzeug=True)
    
    # app.run(debug=True, host="0.0.0.0")

# from flask import Flask, render_template
# from flask_socketio import SocketIO, emit
# import sys

# app = Flask(__name__)
# app.config['SECRET_KEY'] = 'secret!'
# socketio = SocketIO(app, cors_allowed_origins='*')

# @app.route('/')
# def index():
#     return "hello"  # We will create this HTML file for the front-end

# @socketio.on('connect')
# def connect(message):
#     print('new connections', file=sys.stderr)

# @socketio.on('message')
# def handle_message(message):
#     print('received message: ' + message, file=sys.stderr)
#     emit("message", "no")


# if __name__ == '__main__':
#     app.run(debug=True, host="0.0.0.0")
#     # socketio.run(app, debug=True, host="0.0.0.0", allow_unsafe_werkzeug=True)
#     # socketio.run(app)