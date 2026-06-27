# Section 2: Installing the PiCar-X Software

## What this section does

The PiCar-X doesn't drive itself out of the box — it needs some software installed on the Raspberry Pi that knows how to talk to the motors, servos, and sensors. SunFounder (the company that makes the PiCar-X) provides this software for free, and this section walks through installing it.

By the end, you'll be able to run example scripts that move the car, turn the steering, and move the camera.

**Before starting this section, make sure Section 1 (SSH setup) is done** — you should be able to connect to your Pi and see a command prompt.

## Step 1: Connect to your Pi

Open a terminal on your laptop and connect, the same way as Section 1:
```bash
ssh yourusername@picarx.local
```
(or use the IP address if `.local` doesn't work for you)

Everything from here happens inside this SSH session.

## Step 2: Update the system

It's good practice to make sure the Pi's software is up to date before installing anything new:
```bash
sudo apt update && sudo apt full-upgrade -y
```

This might take a few minutes the first time. `sudo` means "run this command with full permissions" — you'll use it a lot, since installing software requires it.

## Step 3: Turn on I2C

The PiCar-X's main control board (called the "Robot HAT") talks to the Pi using a communication standard called **I2C**. It's off by default and needs to be turned on once.

```bash
sudo raspi-config
```

This opens a blue text-based menu. Use the arrow keys to navigate:
1. Go to **Interface Options**
2. Go to **I2C**
3. Select **Yes** to enable it
4. Select **Finish**, and reboot if it asks you to

If it rebooted, just SSH back in afterward.

## Step 4: Install required tools

```bash
sudo apt install -y git python3-pip python3-setuptools python3-smbus
```

Here's what these are:
- **git** — lets us download code from GitHub
- **python3-pip** — lets us install Python packages
- **python3-setuptools** — needed for installing some Python packages
- **python3-smbus** — lets Python talk over the I2C connection we just enabled

## Step 5: Install the robot-hat library

This is the library that knows how to control the Robot HAT board itself (motors, servos, the onboard speaker, etc).

```bash
cd ~
git clone -b 2.5.x https://github.com/sunfounder/robot-hat.git --depth 1
cd robot-hat
sudo python3 install.py
```

`cd ~` means "go to your home folder" — we're doing this so we know exactly where things get downloaded to.

## Step 6: Install the vilib library

This library handles camera-related features (even if you're not using the camera yet, the PiCar-X's example scripts expect this to be installed).

```bash
cd ~
git clone https://github.com/sunfounder/vilib.git --depth 1
cd vilib
sudo python3 install.py
```

## Step 7: Install the picar-x library

This is the main library — the one that actually defines "drive forward," "turn left," and so on.

```bash
cd ~
git clone -b 2.1.x https://github.com/sunfounder/picar-x.git --depth 1
cd picar-x
sudo pip3 install . --break-system-packages
```

This step can take a few minutes. The `--break-system-packages` flag is needed because of how newer versions of Raspberry Pi OS protect their built-in Python installation from accidental changes — it's safe to use here since we're intentionally installing something we want.

## Step 8: Enable the onboard speaker (optional, but recommended)

The Robot HAT has a small speaker built in. This step gets the audio system configured for it (it's also covered in more detail in Section 5, but doing it now means it's ready by the time you need it).

```bash
cd ~/robot-hat
sudo bash i2samp.sh
```

You'll be asked a few yes/no questions — type `y` and press Enter for each. At the end, it will ask to reboot. Let it.

After it reboots, SSH back in.

## Step 9: Try an example script

The picar-x library comes with example scripts to test that everything works.

```bash
cd ~/picar-x/example
ls
```

This lists the available example files. Look for one related to basic movement (often something like `1.move.py` or similar — exact names can vary slightly by version).

**Before running any movement script, make sure the car has room to move and isn't sitting on the edge of a table.**

```bash
sudo python3 1.move.py
```//
(replace the filename with whatever you actually saw in the `ls` output)

If the wheels turn, the steering moves, and the camera pans — the software is installed correctly.

## Troubleshooting

### `ModuleNotFoundError` when running a script

This usually means one of the three libraries (robot-hat, vilib, picar-x) didn't fully install. Go back through Steps 5–7 one at a time and watch closely for any red error text during installation.

### Nothing moves, no error message either

Double check Step 3 — I2C needs to be enabled, and a reboot is sometimes required for it to actually take effect even if `raspi-config` didn't explicitly ask for one.

### `pip3 install` complains about an "externally managed environment"

This is exactly what `--break-system-packages` in Step 7 is for — make sure that flag is included in the command exactly as written.
