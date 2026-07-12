import os
import csv
import time
from datetime import datetime
from flask import Flask, request, jsonify, render_template
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch

app = Flask(__name__)

# --- Configuration ---
MODEL_NAME = "Rta-AILabs/Nandi-Mini-150M-Instruct"
LOG_FILE = "amplify_chat_history.csv"
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"

# --- 1. Model Initialization ---
print(f"--- [AMPLIFY] Initializing Model on {DEVICE}... ---")

tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME, trust_remote_code=True)
model = AutoModelForCausalLM.from_pretrained(
    MODEL_NAME,
    trust_remote_code=True,
    torch_dtype=torch.bfloat16
).to(DEVICE).eval()

print("--- [AMPLIFY] System Ready! ---")

# --- 2. CSV Logging Helper ---
def log_interaction(prompt, response, latency):
    file_exists = os.path.isfile(LOG_FILE)
    fieldnames = ["timestamp", "prompt", "response", "latency_sec", "device"]
    
    with open(LOG_FILE, mode='a', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        if not file_exists:
            writer.writeheader()
            
        writer.writerow({
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "prompt": prompt.replace('\n', ' '), 
            "response": response.replace('\n', ' '),
            "latency_sec": round(latency, 3),
            "device": DEVICE
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
        messages = [{"role": "user", "content": user_prompt}]
        formatted_prompt = tokenizer.apply_chat_template(messages, tokenize=False)
        inputs = tokenizer(formatted_prompt, return_tensors="pt").to(model.device)

        with torch.no_grad():
            generated_ids = model.generate(
                **inputs,
                max_new_tokens=500,
                do_sample=True,
                temperature=0.3,
                top_p=0.9,
                repetition_penalty=1.1,
            )

        generated_ids = [
            output_ids[len(input_ids):] for input_ids, output_ids in zip(inputs.input_ids, generated_ids)
        ]
        response_text = tokenizer.batch_decode(generated_ids, skip_special_tokens=True)[0].strip()

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
    app.run(host='0.0.0.0', port=5000, debug=False)