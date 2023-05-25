import socketio
import smbus
import time
import requests
from escpos.printer import Serial


from enum import Enum

class App_State(Enum):
    IDLE = 0
    PIN = 1     
    HOME = 2
    CHOOSE = 3
    BALANCE = 4
    SNELPIN = 5
    WAIT = 6
    

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
address_receipt = 0x2B

current_state = App_State.IDLE

def main():
    global current_state
    global bus
    global address_rfid
    global address_numpad
    
    while True:
        try:
            if current_state == App_State.IDLE:
                """ 19200 Baud, 8N1, Flow Control Enabled """
                p = Serial(devfile='/dev/serial0', baudrate=19200, bytesize=8, parity='N', stopbits=1, timeout=1.00, dsrdtr=True)
                p.text("Hello World\n")
                
                
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

def https_request(endpoint: str, method: Https_Method, params: dict):
    pass

if __name__ == "__main__":
    main()
