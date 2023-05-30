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
    BLOCKED = 7
    

class Https_Method(Enum):
    GET = 0
    POST = 1     

class sidebutton(Enum):
    L1 = '4'
    L2 = '5'
    L3 = '6'
    L4 = '7'
    R1 = '8'
    R2 = '9'
    R3 = ':'
    R4 = ';'
    
http_session = requests.Session()
http_session.verify = False

socket = socketio.Client(http_session=http_session)

socket.connect("https://127.0.0.1:5000")

bus = smbus.SMBus(1)
address_rfid = 0x2A
address_numpad = 0x2C
address_receipt = 0x2B
address_sidebuttons = 0x2F
address_dispenser = 0x3A

current_state = App_State.IDLE
pin_lock = True


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

                tries = 0
                socket.emit("redirect", "welcome")

                customerUID = request_bytes(address_rfid, 11)
                customerUID = request_bytes(address_rfid, 11)
                print(customerUID)
                socket.emit("sendUID", customerUID)
                current_state = App_State.PIN

            if current_state == App_State.PIN:
                
                   
                socket.on("Correct", correct_pin)

                while(pin_lock):
                    socket.emit("redirect", "pin")

                    pin = ""
                    for _ in range(4):
                        pin += request_bytes(address_numpad, 1, lambda: not pin_lock)
                        print(pin)
                        socket.emit("page_data", "*")
                    print(pin)
                    socket.emit("sendPin", pin)

                    tries += 1
                
                    if (tries > 2):
                        socket.emit("block_message")
                        current_state = App_State.BLOCKED
                        break


            if current_state == App_State.HOME:
                socket.emit("redirect", "home")
                print("home?")

                btn = request_bytes(address_sidebuttons, 1)

                if btn in {sidebutton.L2.value, sidebutton.L3.value}:
                    current_state = App_State.SNELPIN
                
                elif btn in {sidebutton.R2.value, sidebutton.R3.value}:
                    current_state = App_State.BALANCE

                elif btn == sidebutton.L4:
                    end()
            
            if current_state == App_State.BALANCE:
                print("balance is key")
                socket.emit("redirect", "balance")
                socket.emit("show_balance")

                btn = request_bytes(address_sidebuttons, 1)
                
                if btn == sidebutton.R4.value:
                    current_state = App_State.HOME

                elif btn == sidebutton.L4.value:
                    end()
                    
            if current_state == App_State.SNELPIN:
                print("blazingly fast")
                socket.emit("redirect", "snelpin")

                btn = request_bytes(address_sidebuttons, 1)
                time.sleep(1)
                if btn == sidebutton.L1.value:
                    # request 5 emeralds
                    socket.emit("withdrawal", 5)
                    bus.write_byte(address_dispenser, 0)

                elif btn == sidebutton.L2.value:
                    # request 20 emeralds
                    socket.emit("withdrawal", 20)
                    bus.write_byte(address_dispenser, 1)
                
                elif btn == sidebutton.R1.value:
                    #request 50 emeralds
                    socket.emit("withdrawal", 50)
                    bus.write_byte(address_dispenser, 2)

                elif btn == sidebutton.R2.value:
                    #request 75 emeralds
                    socket.emit("withdrawal", 75)
                    bus.write_byte(address_dispenser, 0)
                    bus.write_byte(address_dispenser, 1)
                    bus.write_byte(address_dispenser, 2)
                
                elif btn == sidebutton.R3.value:
                    current_state = App_State.CHOOSE

                elif btn == sidebutton.R4.value:
                    current_state = App_State.HOME

                elif btn == sidebutton.L4.value:
                    end()

            if current_state == App_State.CHOOSE:
                print("Picky pick")

                socket.emit("redirect", "choose")

        except Exception as e:
            print(e)

    
def end():
    global current_state
    global pin_lock
    # reset all local variables
    pin_lock = True
    
    current_state = App_State.IDLE


def correct_pin():
    global current_state
    global pin_lock
    current_state = App_State.HOME
    print(current_state)
    pin_lock = False
    

def request_bytes(addr: str, amount: int, break_state = lambda: False) -> str: 
    data = ""

    while len(data) < amount:
        if break_state():
            return data
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