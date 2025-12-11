/*
 * Program to interface FCT3065-XY Optical Mouse
 * Sensor with Arduino.
 * 
 * This code detects when mouse is moved and also
 * prints the change in x direction and change in y
 * direction in the serial monitor. Please note that a
 * higher frequency results in smaller delta values
 * as the count is reset at every reading. 
 * 
 * 
 * Author: Vineet Sukhthanker
 * Date: 6 October 2020
 * 
 * Adaptations: Leonie Gasser
 * Date: 22 October 2025
 */
 
 // figure out what the max pulling rate is

//Register Addresses from datasheet
#define PROD_ID1 0x00
#define PROD_ID2 0x01
#define MOTION_STATUS 0X02
#define DEL_X 0x03
#define DEL_Y 0x04
#define OP_MODE 0x05
// #define CONF 0x06
#define IMG_QUALITY 0x07
// #define OP_STATE 0x08
// #define W_PROTECT 0x09
// #define SLEEP1_SET 0x0A
// #define ENTER_TIME 0x0B
// #define SLEEP2_SET 0x0C
#define IMG_THRESHOLD 0x0D
#define IMG_RECOG 0x0E

#define IMG_BRIGHT 0x17

#define DEBUG false
#define PLOT_HERE false
#define SLIP_THRESHOLD 5
#define CONTACT_THRESHOLD 0x00
#define FREQUENCY 10 // between 1 and 670 

const int SCLK = 8;
const int SDIO = 4;
const byte noSleep = 0xA0;
bool logStart = false;


void setup() {
  Serial.begin(500000); //used to be 115200
  pinMode (SCLK, OUTPUT);
  mouseInit();
  byte prodId1 = readRegister(PROD_ID1);
  logStart = true;
  if (DEBUG) {
    Serial.print("Device ID: 0x");
    Serial.println(prodId1, HEX);
    Serial.print((prodId1==0x30)?"\nDevice OK":"\nUnknown Device"); // checks for product ID 
  }
}

void loop() {
  if(logStart){
    uint8_t motion = readRegister(MOTION_STATUS); // read motion status register | needs to be read for deltas to update
    if (motion == 0xFF){
      Serial.print("\nBad connection");
      printMode();
    }
    if (DEBUG){
      if (motion & 0x80) Serial.print("\nMoved!");   //new test for moved used to be "if(motion==0x81)"
      else Serial.print("\nno mouvement");
    }
    int8_t delta_x =(int8_t) readRegister(DEL_X); // read delta x register | signed ints
    int8_t delta_y = (int8_t) readRegister(DEL_Y); // read delta y register
    uint8_t quali = readRegister(IMG_QUALITY);
    unsigned long t = micros();
    Serial.print(t); Serial.print(",");
    if (DEBUG || PLOT_HERE) Serial.print("\n contact:");
    Serial.print(quali); Serial.print(",");
    if (DEBUG || PLOT_HERE) Serial.print("\n delta X:");
    Serial.print(delta_x);  Serial.print(",");
    if (DEBUG || PLOT_HERE) Serial.print("\n delta Y:");
    Serial.println(delta_y); 

    int period = 1000000/FREQUENCY;
    int delay = period - 1500; // approximate us if a cycle without added delay
    if (delay > 0){
      delayMicroseconds(delay); // added delay to lower the frequency
    } 
  }
  else{
    Serial.println("no init");
    delay(100);
  } 
}

void mouseInit(void){ // function to initialize optical sensor.
  digitalWrite(SCLK, HIGH);
  digitalWrite(SCLK, LOW);
  delayMicroseconds(1); // tRESYNC = 1us (mentioned in datasheet)
  digitalWrite(SCLK, HIGH);
  delay(320); // tSIWTT = 320ms (mentioned in datasheet)
  digitalWrite(SCLK, LOW);
  if (DEBUG) printMode();
  writeRegister(OP_MODE, noSleep); // disable sleep mode
  if (DEBUG) {
    Serial.print("\nintiation");
    printMode();
  }
}

byte readRegister(byte address) {
  pinMode (SDIO, OUTPUT);
  for (byte i=128; i >0 ; i >>= 1) {
    digitalWrite (SCLK, LOW);
    digitalWrite (SDIO, (address & i) != 0 ? HIGH : LOW);
    digitalWrite (SCLK, HIGH);
  }
  pinMode (SDIO, INPUT);
  delayMicroseconds(3); // tHOLD = 3us (mentioned in datasheet)
  byte res = 0;
  for (byte i=128; i >0 ; i >>= 1) {
    digitalWrite (SCLK, LOW);
    digitalWrite (SCLK, HIGH);
    if( digitalRead (SDIO) == HIGH )
      res |= i;
  }
  delayMicroseconds(3); // tHOLD = 3us min. (mentioned in datasheet)
  return res;
}

void writeRegister(byte address, byte data) {
  address |= 0x80; // MSB indicates write mode.
  pinMode (SDIO, OUTPUT);
  for (byte i = 128; i > 0 ; i >>= 1) {
    digitalWrite (SCLK, LOW);
    digitalWrite (SDIO, (address & i) != 0 ? HIGH : LOW);
    digitalWrite (SCLK, HIGH);
  }
  for (byte i = 128; i > 0 ; i >>= 1) {
    digitalWrite (SCLK, LOW);
    digitalWrite (SDIO, (data & i) != 0 ? HIGH : LOW);
    digitalWrite (SCLK, HIGH);
  }
  delayMicroseconds(100);
}

// leos stuff
void printMode(void){
  uint8_t mode = readRegister(OP_MODE);
  Serial.print("\nmode: 0x");
  Serial.println(mode, HEX);
}

bool contactDectect(void){
  uint8_t quali = readRegister(IMG_QUALITY); // detects no contact at a distance of about 1 cm with == 0x00
  if (quali == CONTACT_THRESHOLD){ // detects no contact at a distance of about 1 cm
    return false; // no contact
  }
  return true;
}


 



