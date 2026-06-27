# Section 1: Setting Up SSH

## What this section does

By the end of this section, your Raspberry Pi will:
- Have its operating system installed
- Be connected to your Wi-Fi automatically every time it powers on
- Let you type commands into it from your laptop, over Wi-Fi, with **no monitor, keyboard, or mouse ever plugged into the Pi**

This is done using something called **SSH** (Secure Shell). Think of it like a remote control for typing: you open a terminal window on your laptop, "log in" to the Pi, and from that point on, anything you type runs on the Pi instead of your laptop. It's all text — no graphics, no mouse — but it's all you actually need to set up and run the car.

## What you'll need

- A Raspberry Pi (this guide assumes a Raspberry Pi 5, but the steps are nearly identical for other models)
- A microSD card (16GB or larger)
- A way to put that microSD card into your everyday computer (a USB SD card reader if your computer doesn't have a slot built in)
- Your Wi-Fi network name and password
- A laptop or desktop computer

## Step 1: Download Raspberry Pi Imager

This is the official, free tool for putting the operating system onto your SD card.

1. Go to **https://www.raspberrypi.com/software/**
2. Download the version for your computer (Windows, Mac, or Linux)
3. Install it like any other application

## Step 2: Flash the SD card

1. Put your microSD card into your computer
2. Open **Raspberry Pi Imager**
3. Click **Choose Device** → select your Pi model (e.g. Raspberry Pi 5)
4. Click **Choose OS** → select **Raspberry Pi OS (64-bit)**
   - This is the full version with a desktop, which is the easiest one to start with
5. Click **Choose Storage** → select your SD card
   - **Double-check you've selected the right drive.** This step erases everything on whatever you pick.
6. Click **Next**

A box will pop up asking if you want to edit settings before writing. Click **Edit Settings**. This step is what lets you skip ever connecting a monitor — pay attention here:

- **General tab:**
  - Set a **hostname** — this is the name your Pi will go by on the network. Something simple like `picarx` works well.
  - Set a **username** and **password** — pick something you'll remember, you'll need it every time you connect.
  - Under **Wireless LAN**, enter your **Wi-Fi network name (SSID)** and **password**.
- **Services tab:**
  - Turn on **Enable SSH**
  - Choose **Use password authentication**

Click **Save**, then click **Yes** to confirm writing. This takes a few minutes. When it's done, eject the card safely from your computer.

## Step 3: Boot the Pi

1. Insert the microSD card into the Raspberry Pi (the slot is on the underside of the board)
2. Connect the Pi to power
3. Wait about a minute for it to boot up and connect to Wi-Fi for the first time

You don't need to connect anything else — no monitor, no keyboard.

## Step 4: Connect over SSH

On your laptop, open a terminal:
- **Mac**: open the **Terminal** app (search for it with Cmd+Space)
- **Windows**: open **PowerShell** or **Command Prompt**
- **Linux**: open your terminal application

Type the following, replacing `yourusername` with the username you set in Step 2, and `picarx` with the hostname you chose:

```bash
ssh yourusername@picarx.local
```

The first time you connect, you'll see a message about the host's authenticity that looks alarming but isn't — it's just confirming you trust this device. Type:

```
yes
```

Then press Enter, and type your password when asked. (Nothing will appear on screen as you type the password — that's normal, it's hidden for security.)

If everything worked, you'll see a welcome message and a new prompt like:
```
yourusername@picarx:~ $
```

**You're now controlling the Pi from your laptop.** Anything you type now runs on the Raspberry Pi, not your laptop.

## Troubleshooting

### `ssh: could not resolve hostname picarx.local`

This means your laptop can't find the Pi by name. Use its IP address instead.

**To find the IP address**, log into your Wi-Fi router's admin page (commonly `192.168.1.1` or `192.168.0.1` — typed into a browser like a website) and look for a connected device with your chosen hostname in the device list.

Once you have the IP address (e.g. `192.168.1.50`), connect with:
```bash
ssh yourusername@192.168.1.50
```

### `ssh: connect to host ... port 22: Connection refused`

This means your laptop *can* reach the Pi, but nothing is listening for SSH connections on it. This most commonly happens if the Pi's IP address changed (for example, after a reboot) and you're trying to connect to its *old* address, which now belongs to a different device or nothing at all.

Double-check the current IP address through your router's admin page, exactly as described above, and try again with the correct one.

### The IP address keeps changing every time I reboot

This is normal default router behavior (called DHCP), but it gets annoying if you have to look up the IP every time. Most routers let you set a **DHCP reservation** — a setting that always assigns the same IP address to a specific device. Check your router's admin page for an option called "DHCP Reservation," "Static IP," or "Address Reservation," and look up your specific router model's instructions if it's not obvious.

### I don't have a router admin page / can't find the IP any other way

If you have a spare monitor, keyboard, and mouse, you can temporarily plug them into the Pi just once, boot it up, and run:
```bash
hostname -I
```
This prints the Pi's current IP address directly. Once you have it, you can unplug everything and go back to SSH from your laptop.
