# Section 7: Wireless Joystick Control

## What this section does

This sets up real joystick control for the car, using:
- An **Arduino** with a joystick attached, reading its position
- Your **laptop**, which reads the Arduino over a USB cable and forwards the joystick position to the car over Wi-Fi
- The **Raspberry Pi**, which receives those commands and drives the car

The joystick itself stays wired to the Arduino, which is wired to your laptop — but the laptop talks to the car wirelessly, so the car itself is free to drive around without being tethered to anything.

**Before starting, make sure Section 2 (installing the PiCar-X software) is complete.**

### Why not connect the joystick straight to the Pi?

This is a fair question. The short answer: this project specifically uses hardware many people already have lying around (an old Arduino and a cheap joystick module), and routing it through a laptop avoids needing to solder or wire anything new directly onto the Robot HAT board, which has limited spare connection points already used by the car's own sensors and motors.

## What you'll need

- An Arduino Uno or Nano
- A 2-axis analog joystick module (often labeled "KY-023" or similar, with pins for GND, +5V, VRx, VRy, and sometimes SW for a button)
- A USB cable to connect the Arduino to your laptop
- The [Arduino IDE](https://www.arduino.cc/en/software) installed on your laptop
- [Python 3](https://www.python.org/downloads/) installed on your laptop, with the `pyserial` package (installed below)

## Step 1: Wire the joystick to the Arduino

| Joystick pin | Arduino pin |
|---|---|
| GND | GND |
| +5V | 5V |
| VRx | A0 |
| VRy | A1 |
| SW (if present) | D2 |

## Step 2: Upload the Arduino sketch

1. Open the [`arduino/joystick_reader.ino`](arduino/joystick_reader.ino) file from this folder in the Arduino IDE
2. Connect your Arduino to your laptop with a USB cable
3. In the Arduino IDE, go to **Tools → Board** and select your exact board (Uno or Nano)
4. Go to **Tools → Port** and select the port your Arduino is connected on
5. Click the **Upload** button (the right-arrow icon)

## Step 3: Verify the joystick is working

Still in the Arduino IDE, open **Tools → Serial Monitor**, and set the baud rate (bottom-right dropdown) to **9600** to match the sketch.

Move the joystick around. You should see lines of three numbers separated by commas, like:
```
512,498,1
612,501,1
1023,234,0
```

The third number drops to `0` only when the joystick's button is pressed (if your joystick module has one).

**Close the Serial Monitor once you've confirmed this works** — only one program can use the USB connection at a time, and we'll need it free for the next step.

## Step 4: Find the Arduino's port name on your laptop

On a Mac, open Terminal and run:
```bash
ls /dev/tty.usb*
```
Note the exact name shown (something like `/dev/tty.usbmodem14201`).

(On Windows, this will instead be a `COM` port like `COM3` — check Device Manager under "Ports (COM & LPT)" with the Arduino plugged in.)

## Step 5: Install pyserial on your laptop

```bash
pip3 install pyserial
```

## Step 6: Set up the bridge script

Open [`mac/joystick_bridge.py`](mac/joystick_bridge.py) from this folder in a text editor, and update these two lines near the top with your actual values:

```python
SERIAL_PORT = "/dev/tty.usbmodem14201"  # from Step 4
PI_IP = "192.168.1.50"                  # your Pi's IP address
```

## Step 7: Set up the receiver script on the Pi

Copy [`pi/joystick_receiver.py`](pi/joystick_receiver.py) onto your Raspberry Pi. The easiest way, if you've cloned this whole repository onto your laptop already, is to copy just this file over using `scp` (run this from your laptop, not the Pi):

```bash
scp pi/joystick_receiver.py yourusername@picarx.local:~/joystick_receiver.py
```

Or, just create the file directly on the Pi over SSH and paste its contents in:
```bash
ssh yourusername@picarx.local
nano ~/joystick_receiver.py
```//
(paste the contents of `pi/joystick_receiver.py`, then save with `Ctrl+O`, Enter, `Ctrl+X`)

## Step 8: Run both scripts

**On the Raspberry Pi** (over SSH):
```bash
sudo python3 ~/joystick_receiver.py
```

**On your laptop**, in a separate terminal window:
```bash
python3 mac/joystick_bridge.py
```
(run this from inside this section's folder, or adjust the path to wherever you saved it)

Move the joystick — the car should respond:
- Push **up/down** → drive forward/backward
- Push **left/right** → steer left/right

## Troubleshooting

### `FileNotFoundError: No such file or directory: '/dev/tty.usbmodemXXXXX'`

The port name in the script doesn't match your actual Arduino's port. Re-run `ls /dev/tty.usb*` and make sure the `SERIAL_PORT` value in `joystick_bridge.py` matches exactly.

### `OSError: [Errno 16] Resource busy`

Something else still has the serial port open — almost always the Arduino IDE's Serial Monitor from Step 3. Close it completely and try again.

### The car drives backward when I push the joystick forward (or vice versa)

This is a quick fix in `mac/joystick_bridge.py`. Find this line:
```python
speed = max(-100, min(100, int((-y_offset / 512) * 100)))
```
If the direction is backward from what you want, remove or add the minus sign in front of `y_offset` and try again.

### The car drifts or creeps on its own even with the joystick centered

Your joystick's resting position might not be exactly `512,512`. Use the Serial Monitor from Step 3 to check what your joystick actually reads at rest, and update `X_CENTER` and `Y_CENTER` in `joystick_bridge.py` to match. You can also increase `DEADZONE` slightly to ignore more drift around center.

### Nothing happens on the car at all, no errors anywhere

- Double-check both scripts are running at the same time, in two separate terminal windows
- Confirm your laptop and Raspberry Pi are on the same Wi-Fi network
- Confirm `PI_IP` in `joystick_bridge.py` matches the Pi's actual current IP address (see Section 1's troubleshooting if you're not sure how to check this)
