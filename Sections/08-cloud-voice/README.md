# Section 8: Making the PiCar-X Speak from the Cloud

## What this section does

This side quest adds a remote vocal broadcaster to the PiCar-X.

You can press a global hotkey on your Mac while driving or watching the camera stream in Google Chrome, type a message into a native popup window, and have the Raspberry Pi speak it instantly through its built-in Robot HAT speaker.

This is a great example of a lightweight client-server setup: the Pi handles the audio playback, while your Mac handles the UI and hotkey listening.

**Before starting, make sure Section 2 (installing the PiCar-X software) is complete.**

## What you'll need

- A Raspberry Pi running the PiCar-X software
- A Mac Mini or another Mac computer
- A working network connection between the Pi and the Mac
- The following packages installed on the Pi:
  - `espeak`
  - `python3-flask`
- The following packages installed on the Mac:
  - `pynput`
  - `requests`

## Files in this folder

- [audio_server.py](audio_server.py): runs on the Raspberry Pi and listens for incoming text over HTTP
- [global_talker.py](global_talker.py): runs on the Mac and opens a popup window when you trigger the hotkey

## Step 1: Prepare the Raspberry Pi

Log into your Raspberry Pi and install the required packages:

```bash
sudo apt-get update
sudo apt-get install espeak python3-flask -y
```

Copy [audio_server.py](audio_server.py) onto the Pi. A simple place to keep it is:

```bash
/home/raspberrypi/picar-x/my_code/audio_server.py
```

Then start the server:

```bash
sudo python3 /home/raspberrypi/picar-x/my_code/audio_server.py
```

Leave that terminal window open while you test the system.

## Step 2: Find your Raspberry Pi IP address

On the Raspberry Pi, open a new terminal tab and run:

```bash
hostname -I
```

Make a note of the Pi's local IP address, such as `192.168.1.42`.

## Step 3: Set up the Mac client

On your Mac, install the Python packages needed for the client:

```bash
pip3 install pynput requests
```

Copy [global_talker.py](global_talker.py) onto your Mac and update the configuration near the top:

```python
PI_IP = "192.168.X.X"
```

Replace that value with the Raspberry Pi IP address you found in Step 2.

## Step 4: Run the Mac controller

Start the script from your Mac terminal:

```bash
python3 global_talker.py
```

The first time you run it, macOS may ask for permission to monitor keyboard input. Open System Settings, go to Privacy & Security, and enable Accessibility for your terminal application.

## Step 5: Test the voice broadcast

1. Open Google Chrome and go to your PiCar-X camera stream or any page you want to keep visible.
2. Press `Command + Shift + S` anywhere on your Mac.
3. A native macOS dialog box should appear.
4. Type a message and press Enter.
5. Your Raspberry Pi should speak the message through its speaker.

## Troubleshooting

### The Mac popup does not appear

Make sure the script is still running and that the terminal has Accessibility permission enabled in macOS.

### The Pi does not speak anything

Check that:
- `espeak` is installed on the Pi
- The Flask server is running
- The IP address in [global_talker.py](global_talker.py) matches the Pi's real IP address
- The Pi and Mac are on the same local network

### The server returns an error

If the server responds with an error, double-check the JSON payload being sent. The client sends a body of the form:

```json
{"text": "your message here"}
```

## Notes

The implementation in this section is intentionally split into two small scripts so the Pi and Mac each handle the part of the system they are best suited for.
