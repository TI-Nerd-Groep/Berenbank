#include <Wire.h>

#define I2C_ADDRESS 0x2F
int BTN_PIN[] = {4,5,6,7,8,9,10,11};
int result = 0;

void requestHandle(){

    Serial.println(result);
    Wire.write(result);
}

void setup(){
    for (int i : BTN_PIN)
    {
        pinMode(i, INPUT_PULLUP);
    }
    Serial.begin(9600);
    
    Wire.begin(I2C_ADDRESS);
    Wire.onRequest(requestHandle);
}

void loop(){
    result = 0;

    for (int i : BTN_PIN)
        if (!digitalRead(i))
            result = i + 48;
}