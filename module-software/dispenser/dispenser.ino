#include "lib/dispenser.h"

Dispenser dispensers[] = {
    Dispenser(3),
    Dispenser(4)
};

void setup(){
    dispensers[0].dispense();
}

void loop(){
    for (Dispenser disp : dispensers)
    {
        disp.loop();
    }
}