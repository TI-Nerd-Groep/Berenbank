#include "lib/ReceiptPrinter.cpp"
#include <SPI.h>
#include <Wire.h>

#define SS_PIN 10
#define RST_PIN 9
#define I2C_ADDRESS 0x2B

ReceiptPrinter tp;

void onRequest(int params){
  String msg [2];
  int index = 0;

  while(1 < Wire.available()) { 
    char c = Wire.read();

    if (c == ';')
      index++;
    else
      msg[index] += c;       
  }

  tp.PrintReceipt(msg[0], msg[1]);
}

void setup()
{
  Wire.begin(I2C_ADDRESS);
  Wire.onReceive(onRequest);
  SPI.begin();
}

void loop()
{

}