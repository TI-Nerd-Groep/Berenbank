#ifndef Dispenser_h
#define Dispenser_h

#define DISPENSE_TIME 500
class Dispenser
{
private:
    int pin;
    unsigned long stopTime;
    bool isRunning;
public:
    Dispenser(int pin){
        this->pin = pin;
        this->stopTime = 0;
        this->isRunning = false;
    }

    void dispense(){
        stopTime = DISPENSE_TIME + (isRunning) ? stopTime : millis();
        isRunning = true;
    }

    void loop(){

        if (!isRunning)
        {
            digitalWrite(pin, 0);
            return;
        }

        digitalWrite(pin, 1);

        if (millis() >= stopTime)
            isRunning = false;
    }
};

#endif