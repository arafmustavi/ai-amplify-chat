import os
import csv
import time
import io
import base64
from datetime import datetime
from flask import Flask, request, jsonify, render_template
from openai import OpenAI
import soundfile as sf
from supertonic import TTS

app = Flask(__name__)

# --- Configuration ---
MODEL_NAME = "qwen2.5-coder-1.5b-instruct"
LOG_FILE = "amplify_chat_history.csv"
LM_STUDIO_BASE_URL = "http://192.168.1.4:50500/v1"

# --- 1. API Client & TTS Initialization ---
print(f"--- [AMPLIFY] Connecting to LM Studio Server at {LM_STUDIO_BASE_URL}... ---")

client = OpenAI(
    base_url=LM_STUDIO_BASE_URL,
    api_key="lm-studio"
)

print("--- [AMPLIFY] Initializing Supertonic TTS... ---")
tts = TTS(auto_download=True)
style = tts.get_voice_style(voice_name="M1")

print("--- [AMPLIFY] System Ready! ---")

# --- 2. CSV Logging Helper ---
def log_interaction(prompt, response, latency):
    file_exists = os.path.isfile(LOG_FILE)
    fieldnames = ["timestamp", "prompt", "response", "latency_sec", "backend"]
    
    with open(LOG_FILE, mode='a', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        if not file_exists:
            writer.writeheader()
            
        writer.writerow({
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "prompt": prompt.replace('\n', ' '), 
            "response": response.replace('\n', ' '),
            "latency_sec": round(latency, 3),
            "backend": "LM-Studio-Remote"
        })

# --- 3. Routes ---

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/ask', methods=['POST'])
def ask():
    data = request.json
    user_prompt = data.get("prompt", "")

    if not user_prompt:
        return jsonify({"error": "No prompt provided"}), 400

    start_time = time.time()

    try:
        # Send payload to LM Studio
        api_response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {"role": "system", "content": "You are an expert software engineer."},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.3,
            max_tokens=500
        )
        
        response_text = api_response.choices[0].message.content.strip()

        latency = time.time() - start_time
        log_interaction(user_prompt, response_text, latency)

        # --- Supertonic TTS Generation for Browser ---
        audio_base64 = ""
        try:
            print("--- [AMPLIFY] Generating Speech... ---")
            wav, _ = tts.synthesize(
                text=response_text,
                lang="en",
                voice_style=style,
                total_steps=8,
                speed=1.05
            )
            
            # Convert the numpy array to WAV bytes in memory
            byte_io = io.BytesIO()
            sf.write(byte_io, wav.squeeze(), 44100, format='WAV')
            byte_io.seek(0)
            
            # Encode the raw bytes to a base64 string for safe JSON transit
            audio_base64 = base64.b64encode(byte_io.read()).decode('utf-8')
            print("--- [AMPLIFY] Audio converted to Base64 successfully ---")
            
        except Exception as tts_error:
            print(f"[TTS ERROR] Failed to generate audio: {tts_error}")

        # Return both text and audio back to the browser
        return jsonify({
            "status": "success",
            "response": response_text,
            "audio": audio_base64,  # This contains the audio data string
            "latency": round(latency, 2)
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)