import os
import csv
import time
from datetime import datetime
from flask import Flask, request, jsonify, render_template
from openai import OpenAI

app = Flask(__name__)

# --- Configuration ---
# Match the exact model identifier loaded in your LM Studio instance
MODEL_NAME = "qwen2.5-coder-1.5b-instruct"
LOG_FILE = "amplify_chat_history.csv"

# If Flask runs on the SAME laptop as LM Studio, use "localhost". 
# If Flask runs on a DIFFERENT device, change "localhost" to your laptop's local IP (e.g., "192.168.1.50")
LM_STUDIO_BASE_URL = "http://192.168.16.111:50500/v1"

# --- 1. API Client Initialization ---
print(f"--- [AMPLIFY] Connecting to LM Studio Server at {LM_STUDIO_BASE_URL}... ---")

client = OpenAI(
    base_url=LM_STUDIO_BASE_URL,
    api_key="lm-studio"  # LM Studio does not strictly require this unless explicit auth is enabled
)

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
        # Send payload using the standardized OpenAI API format structured for Qwen
        api_response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {"role": "system", "content": "You are an expert software engineer."},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.3,
            max_tokens=500
        )
        
        # Extract the text out of the API response JSON object
        response_text = api_response.choices[0].message.content.strip()

        latency = time.time() - start_time
        log_interaction(user_prompt, response_text, latency)

        return jsonify({
            "status": "success",
            "response": response_text,
            "latency": round(latency, 2)
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    # Flask application listening globally on port 5000
    app.run(host='0.0.0.0', port=5000, debug=False)