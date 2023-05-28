#include "lib/dispenser.h"

Dispenser dispensers[2] = {
    Dispenser(3),
    Dispenser(4)
};

void setup(){
    Serial.begin(9600);
    dispensers[0].dispense();
    dispensers[0].dispense();
    dispensers[0].dispense();
    dispensers[0].dispense();

}

void loop(){
    for (size_t i = 0; i < 2; i++)
    {
        dispensers[i].update();
    }
   
   
}