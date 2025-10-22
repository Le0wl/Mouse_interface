/*
 * Program to interface FCT3065-XY Optical Mouse
 * Sensor with Arduino.
 * 
 * This code detects when mouse is moved and also
 * prints the change in x direction and change in y
 * direction in the serial monitor.
 * 
 * Author: Vineet Sukhthanker
 * Date: 6 October 2020
 * 
 * Adaptations: Leonie Gasser
 * Date: 22 October 2025
 */

//Register Addresses from datasheet
#define PROD_ID1 0x00
#define PROD_ID2 0x01
#define MOTION_STATUS 0X02
#define DEL_X 0x03
#define DEL_Y 0x04
#define OP_MODE 0x05
#define CONF 0x06
#define IMG_QUALITY 0x07
#define OP_STATE 0x08
#define W_PROTECT 0x09
#define SLEEP1_SET 0x0A
#define ENTER_TIME 0x0B
#define SLEEP2_SET 0x0C
#define IMG_THRESHOLD 0x0D
#define IMG_RECOG 0x0E

#define DEBUG false

const int SCLK = 8;
const int SDIO = 4;

byte noSleep = 0xA0;

int i = 0;
void setup() {
  Serial.begin(115200);
  pinMode (SCLK, OUTPUT);
  mouseInit();
  
  byte prodId1 = readRegister(PROD_ID1);
  if (DEBUG) {
    Serial.print("Device ID: 0x");
    Serial.println(prodId1, HEX);
    Serial.print((prodId1==0x30)?"\nDevice OK":"\nUnknown Device"); // checks for product ID | leo changed from 31 to30
  }
}

void loop() {
  uint8_t motion = readRegister(MOTION_STATUS); // read motion status register
  if (motion == 0xFF){
      Serial.print("\nBad connection");
      printMode();
    }
  else if (motion & 0x80){ //new test for moved used to be "if(motion==0x81)"
    if (DEBUG) Serial.print("\nMoved!");
    int8_t delta_x =(int8_t) readRegister(DEL_X); // read delta x register | leo thinks it's signed ints
    int8_t delta_y = (int8_t) readRegister(DEL_Y); // read delta y register
    if (DEBUG) Serial.print("\n delta X:");
    Serial.print(delta_x);
    Serial.print(",");
    if (DEBUG) Serial.print(" delta Y:");
    Serial.println(delta_y);  
  }
  delay(50); // leo lowered from 1s delay to 100ms
}

void mouseInit(void) // function to initialize optical sensor.
{
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

void printMode(void){
  uint8_t mode = readRegister(OP_MODE);
  Serial.print("\nmode: 0x");
  Serial.println(mode, HEX);
}

