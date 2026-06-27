"""
PiCar-X Joystick Controller - Laptop Bridge Script

Reads joystick position from the Arduino over USB serial, and forwards it
to the Raspberry Pi over Wi-Fi using UDP network messages.

Before running, update the two values below to match your setup.
"""

import serial
import socket
import time

# ----- UPDATE THESE TWO VALUES FOR YOUR SETUP -----
SERIAL_PORT = "/dev/tty.usbmodem14201"  # Run `ls /dev/tty.usb*` to find yours
PI_IP = "192.168.1.50"                  # Your Raspberry Pi's IP address
# ---------------------------------------------------

BAUD_RATE = 9600
PI_PORT = 9999

# Joystick neutral/center values - most joysticks rest near 512,512
# but yours may differ slightly. Adjust if the car drifts at rest.
X_CENTER = 512
Y_CENTER = 512
DEADZONE = 50  # ignores small drift around center so the car doesn't creep

arduino = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

print(f"Reading joystick from {SERIAL_PORT}, sending to {PI_IP}:{PI_PORT}")
print("Press Ctrl+C to stop.")

time.sleep(2)  # give the Arduino serial connection a moment to settle

try:
    while True:
        line = arduino.readline().decode("utf-8").strip()
        if not line:
            continue

        try:
            x_str, y_str, btn_str = line.split(",")
            x = int(x_str)
            y = int(y_str)
            button = int(btn_str)
        except ValueError:
            continue  # skip malformed lines

        x_offset = x - X_CENTER
        y_offset = y - Y_CENTER

        if abs(x_offset) < DEADZONE:
            x_offset = 0
        if abs(y_offset) < DEADZONE:
            y_offset = 0

        # Steering: -100 (full left) to 100 (full right)
        steering = max(-100, min(100, int((x_offset / 512) * 100)))
        # Speed: -100 (full reverse) to 100 (full forward)
        # Inverted so pushing the joystick UP drives the car FORWARD
        speed = max(-100, min(100, int((-y_offset / 512) * 100)))

        message = f"{steering},{speed},{button}"
        sock.sendto(message.encode(), (PI_IP, PI_PORT))
        print(f"Sent: {message}")

except KeyboardInterrupt:
    print("\nStopping...")
    arduino.close()
    sock.close()
