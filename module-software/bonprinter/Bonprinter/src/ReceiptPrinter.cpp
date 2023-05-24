#include <Adafruit_Thermal.h>
#include <SoftwareSerial.h>
#include <TimeLib.h>

class ReceiptPrinter
{
    SoftwareSerial srl;
    Adafruit_Thermal printer;

public: 
    ReceiptPrinter()
    :
    srl(5, 6),
    printer(&srl)
    {
        
        srl.begin(19200);
        printer.begin();
    }

    void PrintReceipt(String date, float amount)
    {
        WriteHeader();
        WriteDetails(date, amount);
    }

    void WriteHeader()
    {
        printer.boldOn();
        printer.setSize('L');
        // LOGO
        printer.println("TRANSACTIEBON");
        printer.boldOff();
        printer.setSize(12);
        printer.setFont();
    }

    void WriteDetails(String date, float amount)
    {
        printer.println("Datum: " + date);
        printer.println("Bedrag: " + (String) amount);
    }

};