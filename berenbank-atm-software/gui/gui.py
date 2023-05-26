from flask import Flask
from flask import render_template
from flask_socketio import SocketIO, emit, disconnect
import codecs
import smbus

app = Flask(__name__)
socket = SocketIO(app, async_mode=None)

@app.route("/")
def index():
    return render_template('index.html', sync_mode=socket.async_mode)

@socket.on("connect")
def connect():
    redirect("welcome")

@socket.on("redirect")
def redirect(template: str):
    socket.emit("page", get_page_data(template))

@socket.on("page_data")
def update_page_data(data):
    socket.emit("page_data", data)

@socket.on("page_data_balance")
def show_money(data):
    socket.emit("page_data_balance2", data)

@socket.on("sendUID")
def sendUIDToServer(customerUID):
    socket.emit("UID", customerUID)

@socket.on("sendPin")
def sendPinToServer(pinCode):
    socket.emit("pin", pinCode)

@socket.on("correct_pin")
def send_correct_message():
    socket.emit("Correct")

@socket.on("show_balance")
def show_balance():
    socket.emit("balance")

@socket.on("block_message")
def show_blocked():
    socket.emit("show_block")
    socket.emit("blocked")

def get_page_data(folder):
    return codecs.open(f"{app.template_folder}/{folder}/main.html", "r", "utf-8").read()

if __name__ == '__main__':
    socket.run(app, host='127.0.0.1', port=5000, debug=True, ssl_context=('certs/server.crt', 'certs/server.key'))
    
