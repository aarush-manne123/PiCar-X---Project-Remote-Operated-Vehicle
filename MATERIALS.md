# Materials

This page lists every piece of hardware used across this project, organized by which section needs it. If you're just getting started, the **Core Kit** is all you need for Sections 1–5. The rest is only needed if you want to follow that specific later section.

## Core Kit (needed for Sections 1–5)

| Item | Notes |
|---|---|
| SunFounder PiCar-X kit (V2.0) | Includes the car chassis, motors, steering servo, camera pan/tilt servos, ultrasonic sensor, grayscale sensors, Robot HAT board, and battery |
| Raspberry Pi 5 | This guide is written for the Pi 5, but the steps are nearly identical for other Pi models |
| microSD card (16GB or larger) | For installing Raspberry Pi OS |
| A way to read/write that microSD card from your everyday computer | A USB SD card reader, if your computer doesn't have a built-in slot |
| A laptop or desktop computer | For SSH access and running setup commands. Instructions are written for macOS, but Linux/Windows users can adapt the laptop-side steps |
| Wi-Fi network | Both the Pi and your laptop need to be on the same network |
| USB-C cable | For charging the PiCar-X's battery, plugged into the Robot HAT |
| USB-C wall charger (5V/2A or 5V/3A) | A standard phone charger works. Charging from a computer's USB port is often too slow or unreliable — use a wall adapter |

## Section 5: Streaming the Webcam

| Item | Notes |
|---|---|
| USB webcam | Any standard USB webcam that shows up as a UVC (USB Video Class) device will work |

## Section 6: Wireless Joystick Control

| Item | Notes |
|---|---|
| Arduino Uno or Nano | Reads the joystick and sends its position over USB serial |
| 2-axis analog joystick module | Often labeled "KY-023" or similar. Needs GND, +5V, VRx, VRy pins, and ideally a SW (button) pin |
| USB cable for the Arduino | Whatever cable matches your specific Arduino board (often USB-B or USB-C, depending on model) |
| Jumper wires | For connecting the joystick to the Arduino |

## Tools that are helpful but not strictly required

| Item | Notes |
|---|---|
| Small Phillips screwdriver | For assembling the PiCar-X kit and adjusting servo horns during calibration |
| A second device on the same Wi-Fi network | Useful for checking your router's connected-devices list to find the Pi's IP address |

## A note on substitutions

Most of this hardware is interchangeable with similar parts:
- Any Raspberry Pi model that supports Raspberry Pi OS and has enough GPIO pins for the Robot HAT should work, though exact steps (especially around audio and camera handling) may differ slightly on older Pi models.
- Any 2-axis analog joystick module with the same pin layout (GND, +5V, VRx, VRy, SW) should work with the Arduino sketch in Section 6 without changes.
- Any USB webcam recognized as a standard UVC device by Linux should work for Section 6 — no special drivers needed.
