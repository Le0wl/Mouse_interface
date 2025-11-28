// ============================================================
// Arduino Code: 3x Load Cells (HX711) + 1x FSR (A0 分压读取)
// 输出格式: Force1(g),Force2(g),Force3(g),FSR(raw)
// code by Antares
// ============================================================

#include "HX711.h"

// --- HX711 引脚定义 ---
// Load Cell 1: 水平剪切力
const int LOADCELL_DOUT_PIN_1 = 7; //3
const int LOADCELL_SCK_PIN_1  = 6; //2

// Load Cell 2: 竖直法向力
const int LOADCELL_DOUT_PIN_2 = 5;
const int LOADCELL_SCK_PIN_2  = 4;

// // Load Cell 3: 竖直法向力
// const int LOADCELL_DOUT_PIN_3 = 7;
// const int LOADCELL_SCK_PIN_3  = 6;

// // --- FSR 定义 ---
// const int fsrPin = A0;   // FSR 分压点接 A0
// const int fsrResistor = 1000; // 1kΩ 电阻（仅用于说明）

const int FREQUENCY = 100;

// --- HX711 对象 ---
HX711 scale1;
HX711 scale2;
// HX711 scale3;

// --- 校准参数（需要你自己标定！）---
float calibration_factor_1 = 1861.078002;
// float calibration_factor_2 = 2030.073927;
// float calibration_factor_3 = 693.757232;

// --- 偏移量（tare）---
long offset_1 = 0;
// long offset_2 = 0;
// long offset_3 = 0;

void setup() {
  Serial.begin(115200);
  Serial.println("Initializing Load Cells...");

  // --- 初始化 HX711 ---
  scale1.begin(LOADCELL_DOUT_PIN_1, LOADCELL_SCK_PIN_1);
  // scale2.begin(LOADCELL_DOUT_PIN_2, LOADCELL_SCK_PIN_2);
  // scale3.begin(LOADCELL_DOUT_PIN_3, LOADCELL_SCK_PIN_3);

  delay(10);

  if (scale1.is_ready()) Serial.println("Load Cell 1 ready.");
  else Serial.println("Load Cell 1 not found!");

  // if (scale2.is_ready()) Serial.println("Load Cell 2 ready.");
  // else Serial.println("Load Cell 2 not found!");

  // if (scale3.is_ready()) Serial.println("Load Cell 3 ready.");
  // else Serial.println("Load Cell 3 not found!");

  // --- 设置校准系数 ---
  scale1.set_scale(calibration_factor_1);
  // scale2.set_scale(calibration_factor_2);
  // scale3.set_scale(calibration_factor_3);

  // --- 去皮 ---
  Serial.println("Taring Load Cells...");
  offset_1 = scale1.read_average(10);
  // offset_2 = scale2.read_average(10);
  // offset_3 = scale3.read_average(10);

  scale1.set_offset(offset_1);
  // scale2.set_offset(offset_2);
  // scale3.set_offset(offset_3);

  Serial.println("Offsets set.");
  
  // --- 打印 CSV 表头 ---
  Serial.println("Force1(g),Force2(g)");
}

void loop() {
  // --- 读取 HX711 ---
  float force1 = scale1.get_units(1);
  // float force2 = scale2.get_units(1);
  // float force3 = scale3.get_units(1);

  // --- 读取 FSR ---
  // float fsrReading = analogRead(fsrPin); // 0~1023 的原始值
  char buff[48];
  // 保留 2 位小数
  force1 = round(force1 * 100.0) / 100.0;
  // force2 = round(force2 * 100.0) / 100.0;
  // force3 = round(force3 * 100.0) / 100.0;
  // fsrReading = round(fsrReading * 100.0) / 100.0;
  
  // --- 串口输出 CSV 格式 ---

  
  //sprintf(buff, "%.1f,%.1f,%.1f,%.2f", force1, force2, force3, fsrReading);
  //Serial.println(String(force1,2)+","+String(force2,2)+","+String(force3,2)+","+String(fsrReading,2));
  Serial.println(force1, 2); //Serial.print(","); // shear
  //Serial.println(force2, 2); // Serial.print(",");
  // Serial.print(force3, 2); Serial.print(",");
  // Serial.println(fsrReading, 2);

  // // 保留 4 位小数
  // force1 = round(force1 * 10000.0) / 10000.0;
  // force2 = round(force2 * 10000.0) / 10000.0;
  // force3 = round(force3 * 10000.0) / 10000.0;
  // fsrReading = round(fsrReading * 10000.0) / 10000.0;
  
  // // --- 串口输出 CSV 格式 ---
  // Serial.print(force1, 4); Serial.print(",");
  // Serial.print(force2, 4); Serial.print(",");
  // Serial.print(force3, 4); Serial.print(",");
  // Serial.println(fsrReading, 4);

  // delay(100); // 10 Hz 采样
  // int period = 1000000/FREQUENCY;
  // int delay = period; // - approximate us if a cycle without added delay tbd
  // if (delay > 0){
  //   delayMicroseconds(delay); // added delay to lower the frequency
  // } 
}
