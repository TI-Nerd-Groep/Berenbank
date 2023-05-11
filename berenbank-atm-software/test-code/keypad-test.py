import smbus
import time

bus = smbus.SMBus(1)
address = 0x2C

while True:
    data = ""
    
    for i in range(0, 4):
        data += chr(bus.read_byte(address));
    print(data)
