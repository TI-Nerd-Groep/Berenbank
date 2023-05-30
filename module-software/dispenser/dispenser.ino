#include <Wire.h>
#include "lib/dispenser.h"

Dispenser dispensers[3] = {
    Dispenser(3),
    Dispenser(4),
    Dispenser(7)
};

#define I2C_ADDRESS 0x3A

void receiveHandle(int args){
    while (Wire.available())
    {
        int target = Wire.read();
        dispensers[target].dispense();
    }
}

void setup(){
    Wire.onReceive(receiveHandle);
    Wire.begin(I2C_ADDRESS);
    Serial.begin(9600);
}

void loop(){
    for (size_t i = 0; i < 3; i++)
    {
        dispensers[i].update();
    }
}