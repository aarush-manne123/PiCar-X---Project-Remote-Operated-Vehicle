import os
import base64
import requests
import keyboard  # Alternative library that bypasses pyobjc issues

# --- CONFIGURATION ---
PI_IP = "192.168.X.X"  # Replace with your Raspberry Pi's actual local IP address
GROQ_API_KEY = "gsk_YOUR_GROQ_API_KEY"  # Replace with your real Groq API key

def stop_picar():
    # --- ADD YOUR CAR'S STOP COMMAND HERE ---
    # Trigger your specific PiCar-X stop sequence right here
    print("Sending STOP command to PiCar-X...")
    
def analyze_and_speak():
    print("Grabbing snapshot from PiCar...")
    try:
        # 1. Fetch the single frame snapshot from the Raspberry Pi
        response = requests.get(f"http://{PI_IP}:8080/snapshot", timeout=5)
        image_data = response.content
        base64_image = base64.b64encode(image_data).decode('utf-8')

        # 2. Package data and send to Groq API
        print("Sending image to Groq AI...")
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {GROQ_API_KEY}"
        }
        payload = {
            "model": "meta-llama/llama-4-scout-17b-16e-instruct", 
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": "Describe what you see in this image in one short sentence."},
                        {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}}
                    ]
                }
            ],
            "max_tokens": 50
        }
        
        api_res = requests.post("https://api.groq.com/openai/v1/chat/completions", headers=headers, json=payload)
        
        if api_res.status_code == 200:
            ai_text = api_res.json()['choices'][0]['message']['content']
            print(f"AI: {ai_text}")

            # 3. Use macOS system engine to speak out loud
            safe_text = ai_text.replace('"', '') 
            os.system(f'say "{safe_text}"')
        else:
            print(f"Groq API Error {api_res.status_code}: {api_res.text}")

    except Exception as e:
        print(f"Error encountered: {e}")

# --- MAIN ENGINE LOOP ---
print("Listening for hardware keypresses. Press 'a' to analyze. Press Ctrl+C to exit.")

while True:
    keyboard.wait('a')  # Code halts here until 'a' is tapped on the OS level
    print("\n'A' key pressed! Initiating AI sequence...")
    stop_picar()
    analyze_and_speak()
