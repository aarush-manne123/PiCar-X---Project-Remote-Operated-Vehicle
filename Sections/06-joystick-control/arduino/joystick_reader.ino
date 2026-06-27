// PiCar-X Joystick Controller - Arduino Sketch
//
// Reads a 2-axis analog joystick and sends its position over USB serial
// to a laptop, which forwards it on to the Raspberry Pi.
//
// Wiring:
//   Joystick GND -> Arduino GND
//   Joystick +5V -> Arduino 5V
//   Joystick VRx -> Arduino A0
//   Joystick VRy -> Arduino A1
//   Joystick SW  -> Arduino D2 (button, if your joystick module has one)

const int VRX_PIN = A0;
const int VRY_PIN = A1;
const int SW_PIN = 2;

void setup() {
  Serial.begin(9600);
  pinMode(SW_PIN, INPUT_PULLUP);
}

void loop() {
  int xVal = analogRead(VRX_PIN);   // 0-1023
  int yVal = analogRead(VRY_PIN);   // 0-1023
  int button = digitalRead(SW_PIN); // 0 = pressed, 1 = released

  Serial.print(xVal);
  Serial.print(",");
  Serial.print(yVal);
  Serial.print(",");
  Serial.println(button);

  delay(50); // send roughly 20 updates per second
}
