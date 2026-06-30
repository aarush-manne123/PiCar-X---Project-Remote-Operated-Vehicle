import os
import subprocess
from pathlib import Path

from flask import Flask, jsonify, request
from robot_hat import Music

app = Flask(__name__)
sound_system = Music()

BASE_DIR = Path(__file__).resolve().parent
OUTPUT_WAV_PATH = BASE_DIR / "tts_output.wav"


@app.route("/speak", methods=["POST"])
def speak():
    data = request.get_json(silent=True) or {}
    text_to_say = data.get("text", "").strip()

    if not text_to_say:
        return jsonify({"status": "error", "message": "No text provided"}), 400

    print(f"Received text to speak: {text_to_say}")

    subprocess.run(["espeak", "-w", str(OUTPUT_WAV_PATH), text_to_say], check=False)
    sound_system.sound_play(str(OUTPUT_WAV_PATH))

    return jsonify({"status": "success", "message": "Speaking completed"}), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
