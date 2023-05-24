#include <Arduino.h>
#include "ReceiptPrinter.cpp"


void setup()
{
  ReceiptPrinter tp;
  tp.PrintReceipt("DD/MM/YYYY", 123.45);
}

void loop()
{

}