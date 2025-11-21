// Arduino Code for Dual Load Cell Reading with HX711
// Code By Antares Zhang

#include "HX711.h" // Include the HX711 library by bogde

// Define the pins for the first HX711 module
//load cell 1 is horizontal shear force
const int LOADCELL_DOUT_PIN_1 = 3; // Data pin for Load Cell 1
const int LOADCELL_SCK_PIN_1 = 2;  // Clock pin for Load Cell 1

// Define the pins for the second HX711 module
//load cell 2 is the vertical normal force
const int LOADCELL_DOUT_PIN_2 = 5; // Data pin for Load Cell 2
const int LOADCELL_SCK_PIN_2 = 4;  // Clock pin for Load Cell 2

// Define the pins for the Third HX711 module
//load cell 2 is the vertical normal force
const int LOADCELL_DOUT_PIN_3 = 7; // Data pin for Load Cell 2
const int LOADCELL_SCK_PIN_3 = 6;  // Clock pin for Load Cell 2

// Create instances of the HX711 class for each load cell
HX711 scale1;
HX711 scale2;
HX711 scale3;

// --- Calibration Values ---
// IMPORTANT: These are example values. You MUST calibrate your load cells.
// Calibrate by placing a known weight on the load cell and dividing the raw
// reading by the known weight.
// Example: If reading 1,000,000 for 1kg, scale = 1,000,000 / 1 = 1,000,000.
// If your reading is negative, use a negative scale factor.
float calibration_factor_1 = 1861.078002; // Adjust this value after calibration for Load Cell 1
float calibration_factor_2 = 2030.073927; // Adjust this value after calibration for Load Cell 2
float calibration_factor_3 = -686.925; // Adjust this value after calibration for Load Cell 3

// Offset values (tare value at no load)
long offset_1 = -7379; // Will be set in setup() or after taring
long offset_2 = 526431; // Will be set in setup() or after taring
long offset_3 = -1; // Will be set in setup() or after taring

void setup() {
  Serial.begin(115200); // Start serial communication at 19200 baud

  Serial.println("Initializing Load Cells...");

  // Initialize Load Cell 1
  scale1.begin(LOADCELL_DOUT_PIN_1, LOADCELL_SCK_PIN_1);
  delay(100);
  if (scale1.is_ready()) {
    Serial.println("Load Cell 1 is ready.");
  } else {
    Serial.println("Load Cell 1 not found. Check wiring.");
  }

  // Initialize Load Cell 2
  scale2.begin(LOADCELL_DOUT_PIN_2, LOADCELL_SCK_PIN_2);
  delay(100);
  if (scale2.is_ready()) {
    Serial.println("Load Cell 2 is ready.");
  } else {
    Serial.println("Load Cell 2 not found. Check wiring.");
  }

  // Initialize Load Cell 3
  scale3.begin(LOADCELL_DOUT_PIN_3, LOADCELL_SCK_PIN_3);
  delay(100);
  if (scale3.is_ready()) {
    Serial.println("Load Cell 3 is ready.");
  } else {
    Serial.println("Load Cell 3 not found. Check wiring.");
  }

  // Set the scale factor
  scale1.set_scale(calibration_factor_1);
  scale2.set_scale(calibration_factor_2);
  scale3.set_scale(calibration_factor_3);

  Serial.println("Taring Load Cells... Please remove all weight.");
  // Tare (zero out) the scales - takes a few seconds and averages readings
  // This value can be stored in EEPROM for persistence or saved manually after calibration.
  offset_1 = scale1.read_average(10); // Take 10 readings for taring
  offset_2 = scale2.read_average(10); // Take 10 readings for taring
  offset_3 = scale3.read_average(10); // Take 10 readings for taring
  scale1.set_offset(offset_1);
  scale2.set_offset(offset_2);
  scale3.set_offset(offset_3);

  Serial.print("Load Cell 1 Offset: "); Serial.println(offset_1);
  Serial.print("Load Cell 2 Offset: "); Serial.println(offset_2);
  Serial.print("Load Cell 3 Offset: "); Serial.println(offset_3);
  Serial.println("Load cells tared. Ready to read force.");
  Serial.println("Force1(g),Force2(g),Force3(g)"); // CSV Header for Python script
}

void loop() {
  // Read raw values from each load cell
  // .get_value() reads a single raw value
  // .read_average() reads a specified number of raw values and averages them
  // .get_units() converts raw readings to units (grams, kg, lbs etc.) based on calibration_factor
  float force1 = scale1.get_units(1); // Get average of 5 readings for Load Cell 1
  float force2 = scale2.get_units(1); // Get average of 5 readings for Load Cell 2
  float force3 = scale3.get_units(1); // Get average of 5 readings for Load Cell 3

  // Limit to 4 decimal places for consistency with Python rounding
  force1 = round(force1 * 10000.0) / 10000.0;
  force2 = round(force2 * 10000.0) / 10000.0;
  force3 = round(force3 * 10000.0) / 10000.0;

  // Send data over serial in a CSV-friendly format
  Serial.print(force1, 4); // Print force1 with 4 decimal places
  Serial.print(",");      // Separator
  Serial.print(force2, 4); // Print force2 with 4 decimal places and a newline
  Serial.print(",");      // Separator
  Serial.println(force3, 4); // Print force3 with 4 decimal places and a newline

  // Introduce a slight delay to avoid overwhelming the serial port
  delay(100); // Read approximately 10 times per second
}
