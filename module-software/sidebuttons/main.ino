#include <Wire.h>

#define I2C_ADDRESS 0x2F
const int BTN_PIN[] = {4,5,6,7,8,9,10,11};

void requestHandle(){
    int result = 0;

    for (int i : BTN_PIN)
        if (digitalRead(BTN_PIN[i]))
            result = i;

    Wire.write(result);
}

void setup(){
    for (int i : BTN_PIN)
    {
        pinMode(BTN_PIN[i], INPUT_PULLUP);
    }
    
    Wire.begin(I2C_ADDRESS);
    Wire.onRequest(requestHandle);
}

void loop(){

}