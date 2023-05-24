#include <Keypad.h>

const int ROWS = 4;
const int COLS = 4;

char keys[ROWS][COLS] = {
  {'1', '2', '3', 'A'},
  {'4', '5', '6', 'B'},
  {'7', '8', '9', 'C'},
  {'*', '0', '#', 'D'}
};

byte row_pins[ROWS] = {9, 8, 7, 6}; 
byte col_pins[COLS] = {5, 4, 3, 2}; 
Keypad keypad(makeKeymap(keys), row_pins, col_pins, ROWS, COLS);

String get_input(uint8_t len, boolean numeric = false){
    String result = "";

    while (result.length() < len)
    {
        char key = keypad.getKey();
        if (key != NO_KEY)
            if (numeric && isDigit(key) || !numeric)
                result += key;
    }
    return result;
}

void setup(){
    Serial.begin(9600);
}

void loop(){

    Serial.println(get_input(4, true));
}