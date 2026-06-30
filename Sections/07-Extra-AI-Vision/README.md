# Extra AI Vision Add-on

This section explains how to add a simple AI vision feature to the PiCar-X using the Groq API.

## What It Actually Does
Normally, your PiCar-X just drives around and streams video to your screen. This add-on gives it a **"freeze and look"** feature.

When you are controlling the car from your computer and press the **"a"** key:

1. The car instantly stops driving so it doesn't crash or take a blurry photo.
2. It snaps a single, high-quality picture of whatever is right in front of it.
3. An advanced AI looks at that picture and writes a one-sentence description of it.
4. Your computer automatically reads that sentence out loud through its speakers.

Essentially, you are giving your robot car the ability to "tell" you what it sees.

## How It Works Behind the Scenes
To keep things fast and prevent the small Raspberry Pi brain from getting overwhelmed, the work is split between two devices:

### 1. The Raspberry Pi (The Car)
The Pi handles the physical hardware and camera.
It runs a small camera server that streams live video during normal driving.
When your computer asks for a `/snapshot`, the Pi grabs the most recent clean frame and sends it back.

### 2. Your Computer (The Brains & Voice)
Your computer listens for the **"a"** key, downloads the snapshot from the car, sends it to Groq AI for analysis, then speaks the AI description out loud.

- Press **"a"** on your keyboard.
- The car stops.
- The computer fetches a still image from the Pi.
- The image is sent to Groq AI.
- The AI returns a one-sentence description.
- Your computer speaks that sentence using its text-to-speech engine.

## Why Use Groq AI?
Running a heavy AI model directly on the Raspberry Pi would make the car lag, freeze, or drain its battery quickly.
This setup offloads the actual image understanding to the cloud.
Groq is designed for extreme speed, so the delay between pressing **"a"** and hearing the description is just a couple of seconds.

## Files in This Folder
Create the following two Python files in this same folder and run them on the appropriate devices.

### `picar_camera_server.py`
- Run on the Raspberry Pi.
- Provides the camera stream and a `/snapshot` endpoint.
- Configures the Pi camera and serves live MJPEG plus a single-frame snapshot.

### `ai_vision.py`
- Run on your computer.
- Listens for the **"a"** key.
- Stops the car, downloads the snapshot, sends it to Groq, and uses text-to-speech.

## Setup Notes
- Replace `PI_IP` in `ai_vision.py` with your Raspberry Pi's local IP address.
- Replace `GROQ_API_KEY` with your Groq API key.
- Make sure the Pi camera server is reachable from your computer.
- Install required Python packages on each device.

## Recommended Workflow
1. Start `picar_camera_server.py` on the Raspberry Pi.
2. Start `ai_vision.py` on your computer.
3. Control the car normally.
4. Press **"a"** to let the car freeze, capture, analyze, and speak what it sees.

## Notes
This README intentionally describes the feature and references separate code files.
Do not copy the full implementation into this README; put the actual scripts in the file names above.
