import socketio
import smbus
import time
import requests
from enum import Enum

class App_State(Enum):
    IDLE = 0
    PIN = 1     
    HOME = 2

class Https_Method(Enum):
    GET = 0
    POST = 1     
    
http_session = requests.Session()
http_session.verify = False

socket = socketio.Client(http_session=http_session)

socket.connect("https://127.0.0.1:5000")

bus = smbus.SMBus(1)
address_rfid = 0x2a
address_numpad = 0x2c

current_state = App_State.IDLE

def main():
    global current_state
    global bus
    global address_rfid
    global address_numpad
    
    while True:
        try:
            if current_state == App_State.IDLE:
                send_message("12/13/2023;123.80")
                socket.emit("redirect", "welcome")

                customerUID = request_bytes(address_rfid, 11)
                socket.emit("sendUID", customerUID)
                print(customerUID)
                current_state = App_State.PIN

            if current_state == App_State.PIN:
                socket.emit("redirect", "pin")

                pin = ""
                for _ in range(4):
                   pin += request_bytes(address_numpad, 1)
                   socket.emit("page_data", "*")
                socket.emit("sendPin", pin)
                print(pin)

                current_state = App_State.PIN

            if current_state == App_State.HOME:
                socket.emit("redirect", "home")
                print("home?")
        except Exception as e:
            print(e)

    

def request_bytes(addr: str, amount: int) -> str: 
    data = ""

    while len(data) < amount:
        char = chr(bus.read_byte(addr));
    
        if char == chr(0):
            data = ""
        else:
            data += char

    return data

def send_message(addr: str, msg: str):
    for char in msg:
        bus.write_byte(addr, char)


def https_request(endpoint: str, method: Https_Method, params: dict):
    pass

if __name__ == "__main__":
    main()


