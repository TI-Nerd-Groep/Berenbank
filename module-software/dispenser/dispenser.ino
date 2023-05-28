#include <Wire.h>

#include "lib/dispenser.h"

#define I2C_ADDRESS 0x2E

Dispenser dispensers[2] = {
    Dispenser(3),
    Dispenser(4)
};

void receiveHandle(int args){
    while(1 < Wire.available()) { 
        int disp = Wire.read();
        dispensers[disp].dispense();
    }
}

void setup(){
    Wire.begin(I2C_ADDRESS);
    Wire.onReceive(requestHandle);

    Serial.begin(9600);
}

void loop(){
    for (size_t i = 0; i < 2; i++)
    {
        dispensers[i].update();
    }
   
   
}