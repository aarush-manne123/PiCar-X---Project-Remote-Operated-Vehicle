"""
PiCar-X Joystick Controller - Raspberry Pi Receiver Script

Listens for joystick position messages sent over Wi-Fi (UDP) from the
laptop bridge script, and converts them into PiCar-X movement commands.

Includes a safety feature: if no message is received for more than a
second (for example, if the laptop disconnects or Wi-Fi drops), the car
automatically stops instead of continuing to drive blindly.
"""

import socket
import time
from picarx import Picarx

px = Picarx()

UDP_IP = "0.0.0.0"   # listen on all network interfaces
UDP_PORT = 9999

MAX_SPEED = 40         # top speed, out of 100
MAX_STEER_ANGLE = 30   # maximum steering angle in degrees

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))
sock.settimeout(0.5)

print(f"Listening for joystick commands on port {UDP_PORT}...")
print("Press Ctrl+C to stop.")

last_received_time = time.time()

try:
    while True:
        try:
            data, addr = sock.recvfrom(1024)
            message = data.decode()
            steering_str, speed_str, button_str = message.split(",")

            steering_pct = int(steering_str)  # -100 to 100
            speed_pct = int(speed_str)        # -100 to 100

            angle = int((steering_pct / 100) * MAX_STEER_ANGLE)
            speed = int((speed_pct / 100) * MAX_SPEED)

            px.set_dir_servo_angle(angle)

            if speed > 5:
                px.forward(speed)
            elif speed < -5:
                px.backward(abs(speed))
            else:
                px.stop()

            last_received_time = time.time()

        except socket.timeout:
            # No data received recently - stop the car as a safety measure
            if time.time() - last_received_time > 1.0:
                px.stop()

except KeyboardInterrupt:
    print("\nStopping...")
    px.stop()
    px.set_dir_servo_angle(0)
