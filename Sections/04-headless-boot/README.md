# Section 4: Running Headless on Boot

## What this section does

So far, every script has needed you to SSH in and type a command to start it. This section sets up a script to **start automatically the instant the car powers on** — no laptop, no SSH session, nothing except plugging in the power.

This uses a Linux feature called **systemd**, which is the standard tool for managing background services and startup tasks.

**Before starting, make sure Section 2 (installing the software) is complete**, and decide which script you want to run automatically (any of the example scripts from the `picar-x/example` folder will work for this guide).

## Step 1: Connect and find your script

```bash
ssh yourusername@picarx.local
ls ~/picar-x/example
```

Note the exact filename of the script you want to auto-start, and its full path. For this guide, we'll use `~/picar-x/example/4.avoiding_obstacles.py` as an example — replace this with whichever script you actually want.

## Step 2: Create a service file

A "service file" is a small text file that tells systemd what to run and how.

```bash
sudo nano /etc/systemd/system/picarx.service
```

This opens a text editor called `nano` directly in your terminal. Paste in the following, **replacing `yourusername` and the script path with your actual values**:

```ini
[Unit]
Description=PiCar-X Autostart Script
After=multi-user.target

[Service]
Type=simple
WorkingDirectory=/home/yourusername/picar-x/example
ExecStart=/usr/bin/python3 /home/yourusername/picar-x/example/4.avoiding_obstacles.py
Restart=on-failure
RestartSec=5
User=root

[Install]
WantedBy=multi-user.target
```

What this means, line by line:
- **Description** — just a human-readable label
- **WorkingDirectory** — the folder the script runs from (some scripts expect to find files relative to their own folder)
- **ExecStart** — the exact command to run
- **Restart=on-failure** — if the script crashes, try running it again automatically
- **User=root** — runs with full permissions, which the car's motors/sensors need

To save in `nano`: press `Ctrl+O`, then `Enter` to confirm, then `Ctrl+X` to exit.

## Step 3: Enable and start it

```bash
sudo systemctl daemon-reload
sudo systemctl enable picarx.service
sudo systemctl start picarx.service
```

- `daemon-reload` tells systemd to notice the new file you created
- `enable` makes it start automatically every time the Pi boots, from now on
- `start` runs it right now, immediately, so you can check it works without rebooting

## Step 4: Check it's running

```bash
sudo systemctl status picarx.service
```

Look for the words `active (running)`, usually shown in green. If your script controls movement, the car should already be doing something.

To see live output from the script (useful for spotting errors):
```bash
journalctl -u picarx.service -f
```
Press `Ctrl+C` to stop watching this — it doesn't stop the actual service, just the log view.

## Step 5: Test it for real

```bash
sudo reboot
```

Your SSH session will disconnect (that's expected — the Pi is restarting). Unplug it from your laptop entirely if you want a true test. Power it back on, wait about a minute, and the script should start running entirely on its own.

## Useful commands going forward

| Command | What it does |
|---|---|
| `sudo systemctl stop picarx.service` | Stop it right now |
| `sudo systemctl restart picarx.service` | Restart it (useful after editing the script) |
| `sudo systemctl disable picarx.service` | Stop it from starting automatically on boot |

## An important safety note

Once this is set up, **the car will start moving on its own every time you power it on** — including times you just wanted to plug it in to test something else, or charge it. Keep this in mind so it doesn't unexpectedly drive off a table or desk. If you want it to wait for some kind of signal before doing anything, that requires changing the script itself to wait for a button press or similar trigger, which is outside the scope of this guide but worth knowing as an option.

## Troubleshooting

### `systemctl status` shows `failed` instead of `active`

Run `journalctl -u picarx.service -f` and look at the actual error message. The most common cause is a typo in the file path inside `ExecStart` — double check it matches exactly where your script actually lives (`ls ~/picar-x/example` will confirm the real filename and path).

### It works when I run it manually with `sudo python3 script.py`, but not as a service

Double-check the `WorkingDirectory` line matches the folder the script actually expects to run from — some scripts load other files using paths relative to their own folder, and if the working directory is wrong, those files won't be found.
