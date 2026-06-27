# Section 6: Streaming the Webcam

## What this section does

This sets up a **USB webcam** plugged into the Pi to stream live video that you can watch in any browser on your network — handy for driving the car while watching where it's going.

This uses a tool called **mjpg-streamer**, which reads from a standard USB webcam and serves the video feed over a simple web address.

**Before starting, make sure Section 1 (SSH setup) is complete.** You'll also need a USB webcam plugged into the Raspberry Pi.

## Step 1: Connect to your Pi

```bash
ssh yourusername@picarx.local
```

## Step 2: Install build tools

mjpg-streamer needs to be compiled from its source code, so we need some development tools first:

```bash
sudo apt update
sudo apt install cmake libjpeg62-turbo-dev imagemagick libv4l-dev build-essential -y
```

## Step 3: Download and build mjpg-streamer

```bash
cd ~
git clone https://github.com/jacksonliam/mjpg-streamer.git
cd mjpg-streamer/mjpg-streamer-experimental
make
sudo make install
```

The `make` step compiles the program from its source code, so it can take a couple of minutes. Watch for any red error text — if it finishes without errors, it worked.

## Step 4: Confirm your webcam is detected and find its device name

```bash
v4l2-ctl --list-devices
```

This lists connected cameras and which `/dev/videoX` name each one uses. Most setups with a single webcam will show `/dev/video0`, but note the exact one shown for your camera.

## Step 5: Start the stream

```bash
mjpg_streamer -i "input_uvc.so -d /dev/video0 -r 640x480 -f 30" -o "output_http.so -p 8080 -w /usr/local/share/mjpg-streamer/www"
```

Adjust `/dev/video0` if Step 4 showed a different device name. A breakdown of the settings:
- `-r 640x480` — the video resolution
- `-f 30` — frames per second
- `-p 8080` — the network port the stream will be available on

**Leave this command running** — don't close the terminal or press Ctrl+C, or the stream will stop. (See the Troubleshooting section below for how to run this in the background instead, so you can close the terminal and keep using SSH for other things.)

## Step 6: Watch the stream

On your laptop (or any device on the same Wi-Fi network), open a web browser and go to:

```
http://picarx.local:8080/?action=stream
```

(replace `picarx.local` with your Pi's hostname or IP address if needed — see Section 1's troubleshooting if `.local` doesn't work for you)

You should see a live video feed from the webcam. There's also a nicer built-in viewer page at:

```
http://picarx.local:8080/
```

## Troubleshooting

### `make` fails partway through with errors

Double check Step 2 completed without errors first — a missing development package is the most common cause of build failures. Try re-running the install command from Step 2 and watch closely for anything that says "unable to locate package," then search for the correct current package name for your OS version if so.

### The browser shows nothing, or "can't connect"

- Make sure the `mjpg_streamer` command from Step 5 is still actually running in your SSH terminal — if that terminal window closed, the stream stopped.
- Double-check you're using the correct IP address or hostname, and that your laptop is on the same Wi-Fi network as the Pi.

### I want the stream to keep running after I close my terminal

Run the command with `nohup` and put it in the background:
```bash
nohup mjpg_streamer -i "input_uvc.so -d /dev/video0 -r 640x480 -f 30" -o "output_http.so -p 8080 -w /usr/local/share/mjpg-streamer/www" > ~/mjpg.log 2>&1 &
```
This lets you close the SSH session and the stream keeps running. To stop it later, you'll need to find and stop the process:
```bash
pkill mjpg_streamer
```
