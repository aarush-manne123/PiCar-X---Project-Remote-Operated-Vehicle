# PiCar-X Project

This repository documents how I set up, calibrated, and extended my [SunFounder PiCar-X](https://www.sunfounder.com/products/picar-x) running on a Raspberry Pi 5 with **Raspberry Pi OS**.

It's written so that **anyone can follow along** — whether you've never touched a Raspberry Pi before, or you're an experienced developer. Every command is explained, not just listed. If you're new to this, don't skip the explanations — they're there so you understand *why* you're typing something, not just *what* to type.

## What this car can do, after following this guide

- Be controlled entirely over Wi-Fi from a laptop terminal — no monitor or keyboard ever needed on the Pi itself
- Run the official PiCar-X software for driving, steering, and using its sensors
- Be properly calibrated so the steering and camera sit straight
- Automatically start a script the instant it powers on, with no laptop involved
- Stream a live webcam feed to any browser on the network
- Be driven with a real joystick, wired to an Arduino, wirelessly bridged to the car over Wi-Fi
- Speak text remotely from a Mac using a cloud-style hotkey and popup interface

## Materials

See **[Materials](MATERIALS.md)** for the full list of hardware used, organized by which section needs it.

## Sections

Each section below is self-contained, with its own README and, where relevant, its own code. Go through them in order — later sections assume earlier ones are already done.

| # | Section | What it covers |
|---|---|---|
| 1 | [Setting up SSH](Sections/01-ssh-setup/README.md) | Flashing Raspberry Pi OS, connecting over Wi-Fi, no monitor needed |
| 2 | [Installing the PiCar-X Software](Sections/02-picarx-software/README.md) | Getting the car's own libraries onto the Pi |
| 3 | [Calibrating the Car](Sections/03-calibration/README.md) | Zeroing the steering and camera servos |
| 4 | [Running Headless on Boot](Sections/04-headless-boot/README.md) | Making a script start automatically with no laptop involved |
| 5 | [Streaming the Webcam](Sections/05-webcam-streaming/README.md) | Watching a live video feed in your browser |
| 6 | [Wireless Joystick Control](Sections/06-joystick-control/README.md) | Driving the car with an Arduino + joystick over Wi-Fi |
| 7 | [Extra AI Vision](Sections/07-Extra-AI-Vision/README.md) | Click "a" on your keyboard and have Groq AI analyze your image |
| 8 | [Cloud Voice Broadcast](Sections/08-cloud-voice/README.md) | Trigger speech from a Mac hotkey and a popup dialog |

## A note on troubleshooting

Almost everything in here came from genuinely debugging real problems along the way. Each README includes a **Troubleshooting** section at the bottom with the specific issues that came up, in case they help you too.

## How this project is organized

If you're new to GitHub: this whole repository is just a folder of text files and code, stored online. The `sections/` folder contains one subfolder per topic above, and each subfolder has its own `README.md` (instructions) plus any code files that go with it. You don't need to download anything special to read it — GitHub displays README files automatically when you open a folder.
