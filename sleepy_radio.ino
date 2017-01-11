#include <RTCZero.h>

#include <SPI.h>
#include <RH_RF95.h>

#include <ArduinoJson.h>

#define DEVID 6

#define RESOLUTION 4096

  // for feather m0  
#define RFM95_CS 8
#define RFM95_RST 4
#define RFM95_INT 3

//#define RF95_FREQ 915.0
#define RF95_FREQ 868.0

RTCZero zerortc;


// Set how often alarm goes off here
const byte alarmSeconds = 2;
const byte alarmMinutes = 0;
const byte alarmHours = 0;


volatile bool alarmFlag = false; // Start awake

// Singleton instance of the radio driver
RH_RF95 rf95(RFM95_CS, RFM95_INT);

// Blinky on receipt
#define LED 13

// Voltage PIN
#define VBATPIN A7

void setup()
{
  Serial.begin(9600);
  delay(3000); // Wait for console
  
  pinMode(LED_BUILTIN, OUTPUT);
  digitalWrite(LED_BUILTIN, LOW);

  //radio manual reset
  digitalWrite(RFM95_RST, LOW);
  delay(10);
  digitalWrite(RFM95_RST, HIGH);
  delay(10);


   while (!rf95.init()) {
    Serial.println("LoRa radio init failed");
    while (1);
  }
  Serial.println("LoRa radio init OK!");
 
  // Defaults after init are 434.0MHz, modulation GFSK_Rb250Fd250, +13dbM
  if (!rf95.setFrequency(RF95_FREQ)) {
    Serial.println("setFrequency failed");
    while (1);
  }
  Serial.print("Set Freq to: "); Serial.println(RF95_FREQ);
  
  // Defaults after init are 434.0MHz, 13dBm, Bw = 125 kHz, Cr = 4/5, Sf = 128chips/symbol, CRC on
 
  // The default transmitter power is 13dBm, using PA_BOOST.
  // If you are using RFM95/96/97/98 modules which uses the PA_BOOST transmitter pin, then 
  // you can set transmitter powers from 5 to 23 dBm:
  rf95.setTxPower(23, false);

  

  zerortc.begin(); // Set up clocks and such
  
  resetAlarm();  // Set alarm
  zerortc.attachInterrupt(alarmMatch); // Set up a handler for the alarm
}

int16_t packetnum = 0;  // packet counter, we increment per xmission

void loop()
{
  if (alarmFlag == true) {

    
        alarmFlag = false;  // Clear flag
        digitalWrite(LED_BUILTIN, HIGH);
        delay(1000);
         digitalWrite(LED_BUILTIN, LOW);
        Serial.println("Alarm went off - I'm awake!");


float t = 3.2;
float h = 2.;

        StaticJsonBuffer<200> jsonBuffer;
  JsonObject& root = jsonBuffer.createObject();
  root["id"] = DEVID;
  root["packetnum"] = packetnum;
  JsonObject& data = root.createNestedObject("data");
  data["temp"] = double_with_n_digits(t,2);
  data["humidity"] = double_with_n_digits(h,2);
  data["A0"] = analogRead(A0);
  data["A1"] = analogRead(A1);
  data["A2"] = analogRead(A2);
  data["A3"] = analogRead(A3);
  data["A4"] = analogRead(A4);
  data["A5"] = analogRead(A5);

  char buf[251];
  root.printTo(buf, sizeof(buf));
  buf[sizeof(buf)-1] = 0;
  
  Serial.print("Sending "); Serial.println(buf);


  rf95.send((uint8_t *)buf, sizeof(buf));

  
  Serial.println("Waiting for packet to complete..."); delay(10);
    
  rf95.waitPacketSent();

  packetnum++; // update the packet number
  
  
     digitalWrite(LED,HIGH);
    delay(50);
    digitalWrite(LED, LOW);



        
      }
  resetAlarm();  // Reset alarm before returning to sleep
  Serial.println("Alarm set, going to sleep now.");
  //digitalWrite(LED_BUILTIN, LOW);
  delay(1000);
  zerortc.standbyMode();    // Sleep until next alarm match
}



void alarmMatch(void)
{
  alarmFlag = true; // Set flag
}

void resetAlarm(void) {
  byte seconds = 0;
  byte minutes = 0;
  byte hours = 0;
  byte day = 1;
  byte month = 1;
  byte year = 1;
  
  zerortc.setTime(hours, minutes, seconds);
  zerortc.setDate(day, month, year);

  zerortc.setAlarmTime(alarmHours, alarmMinutes, alarmSeconds);
  zerortc.enableAlarm(zerortc.MATCH_HHMMSS);
}
