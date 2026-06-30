import subprocess

import requests
from pynput import keyboard

# --- CONFIGURATION ---
PI_IP = "192.168.X.X"  # Replace with your Raspberry Pi IP address
PI_AUDIO_URL = f"http://{PI_IP}:5000/speak"


def get_mac_input():
    """Spawns a native macOS AppleScript dialog box over all active windows."""
    applescript = (
        'display dialog "Type what you want the PiCar to say:" '
        'default answer "" '
        'buttons {"Cancel", "Speak"} default button "Speak" '
        'with title "PiCar-X Vocal Controller"'
    )
    try:
        process = subprocess.run(
            ["osascript", "-e", applescript],
            capture_output=True,
            text=True,
            check=False,
        )
        output = process.stdout.strip()
        if "text returned:" in output:
            return output.split("text returned:")[1]
    except Exception as exc:
        print(f"Popup error: {exc}")
    return None


def trigger_speech():
    user_message = get_mac_input()
    if user_message and user_message.strip():
        print(f"Broadcasting: '{user_message}'")
        try:
            response = requests.post(PI_AUDIO_URL, json={"text": user_message}, timeout=5)
            if response.status_code == 200:
                print("⚡ Broadcast successful!")
            else:
                print(f"❌ Server Error: {response.status_code}")
        except Exception as exc:
            print(f"❌ Network Error: {exc}")


# Tracking held keys to prevent thread blocking or memory segfaults
current_keys = set()


def on_press(key):
    if key == keyboard.Key.cmd or key == keyboard.Key.cmd_r:
        current_keys.add("cmd")
    elif key == keyboard.Key.shift or key == keyboard.Key.shift_r:
        current_keys.add("shift")
    elif hasattr(key, "char") and key.char == "s":
        current_keys.add("s")

    if "cmd" in current_keys and "shift" in current_keys and "s" in current_keys:
        trigger_speech()


def on_release(key):
    if key == keyboard.Key.cmd or key == keyboard.Key.cmd_r:
        current_keys.discard("cmd")
    elif key == keyboard.Key.shift or key == keyboard.Key.shift_r:
        current_keys.discard("shift")
    elif hasattr(key, "char") and key.char == "s":
        current_keys.discard("s")


print("==================================================")
print("   Global Mac Listener Active (Zero-Segfault)     ")
print("   Press [ Command + Shift + S ] anywhere on Mac  ")
print("   Press Ctrl+C in this terminal to quit.         ")
print("==================================================")

with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()
