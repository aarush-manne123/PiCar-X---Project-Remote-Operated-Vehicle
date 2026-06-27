# Section 3: Calibrating the Car

## What this section does

Calibration tells the software where "straight" and "centered" actually are on your specific car. Without it, the steering might sit crooked, or the camera might tilt at an odd angle even when no command has been given.

This matters because each servo (the small motors that turn the wheels and move the camera) is attached by hand during assembly, and they don't always land in a perfectly centered position. Calibration fixes that mismatch in software.

**Before starting, make sure Section 2 (installing the software) is complete.**

## Step 1: Connect and navigate to the example folder

```bash
ssh yourusername@picarx.local
cd ~/picar-x/example
ls
```

Look for a file related to calibration — it's often named something like `calibration.py` or numbered alongside the other examples.

## Step 2: Run the calibration script

```bash
sudo python3 calibration.py
```//
(use the exact filename you saw from `ls`)

This script will show you a menu of which part to calibrate (steering, camera pan, camera tilt) and let you nudge each one with keyboard keys (commonly `W`/`S` to adjust, and a number key to pick which servo).

## Step 3: Adjust each servo

For each part:
1. Select it (usually by pressing a number key)
2. Use `W` and `S` to move it left/right or up/down in small steps
3. Watch the actual car — not just the screen — and stop adjusting once that part is sitting straight:
   - **Steering**: wheels pointing straight ahead
   - **Camera pan**: camera facing directly forward
   - **Camera tilt**: camera level, neither looking up nor down
4. Save/confirm that calibration value (the script will tell you the key for this — often a specific key to "set" or "save")

Repeat for each servo, then exit the script.

## A note on doing this safely

If a servo is straining, jerking, or making a grinding noise as you adjust it, **stop immediately** — don't keep pressing the key in that direction. That sound means the mechanical part (like the plastic arm attached to the servo) is hitting a hard limit it physically cannot move past. Continuing to push it can strip the small gears inside the servo motor or pop the arm off its mount.

If this happens:
1. Move the servo back the *other* way, away from the strain
2. Power off the car
3. Unscrew the small plastic arm (called a "horn") from the part that was straining
4. Re-run the calibration script and center that specific servo using the keys, without the horn attached
5. With the servo now sitting at its true center, re-attach the horn so the wheel/camera is facing straight *at that position*
6. Screw it back in, and re-run calibration to confirm it now moves freely across its full range without straining at either end

This is a normal part of building one of these kits by hand — it's not a sign that anything is broken.

## Troubleshooting

### The car or camera drifts to one extreme during calibration

This is almost always the battery running low. Servos that are losing power can get pulled to one side instead of holding their commanded position, and motors will feel weaker at the same time. Charge the battery fully (using a proper wall USB-C charger, not a laptop's USB port, which often can't supply enough power) and try again.

### After calibrating, the wheels turn the wrong direction when I press a movement key

Double-check you saved/confirmed the calibration value for that specific servo before exiting the script — some calibration tools only apply your changes after you explicitly confirm them, otherwise they're discarded when the script closes.
