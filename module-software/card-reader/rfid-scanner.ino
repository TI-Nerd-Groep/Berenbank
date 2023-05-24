#include <SPI.h>
#include <MFRC522.h>
#include <Wire.h>
 
#define SS_PIN 10
#define RST_PIN 9
#define I2C_ADDRESS 0x2A
MFRC522 mfrc522(SS_PIN, RST_PIN);   // Create MFRC522 instance.

String content= "";
char data[12];
int index = 0;

void sendData()
{
  Wire.write(data[index]);
  ++index;
  if (index >= 11) {
    index = 0;
  }
}
 
void setup() 
{
  Serial.begin(9600);   // Initiate a serial communication
  Wire.begin(I2C_ADDRESS);
  Wire.onRequest(sendData);
  SPI.begin();      // Initiate  SPI bus
  mfrc522.PCD_Init();   // Initiate MFRC522
  Serial.println("Approximate your card to the reader...");
  Serial.println();
}
void loop() 
{
  // Look for new cards
  if ( ! mfrc522.PICC_IsNewCardPresent()) 
  {
    return;
  }
  // Select one of the cards
  if ( ! mfrc522.PICC_ReadCardSerial()) 
  {
    return;
  }
  //Show UID on serial monitor
  Serial.print("UID tag : ");
  byte letter;
  for (byte i = 0; i < mfrc522.uid.size; i++) 
  {
     content.concat(String(mfrc522.uid.uidByte[i] < 0x10 ? " 0" : " "));
     content.concat(String(mfrc522.uid.uidByte[i], HEX));
  }
  content.toUpperCase();
  content.substring((1)).toCharArray(data, 12);
  Serial.print(content.substring(1));
  Serial.println();
  content = "";
} 
