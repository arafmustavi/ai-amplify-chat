# AMPLIFY AI ECOSYSTEM ⚡

AMPLIFY is a locally-hosted, high-performance AI ecosystem. It features a sleek "Glassmorphism" chat interface and a private, password-protected analytics dashboard to track model performance and user interactions in real-time.

![AMPLIFY Chat Interface](assets/screenshot.png)

-----

## ✨ Enhanced Features

  * **Public Chat Interface:** A minimalist, modern UI featuring **Markdown Support** for bold text, lists, and code blocks.
  * **Private Analytics Dashboard:** A dedicated Streamlit app to visualize usage trends, average latency, and chat history.
  * **Live Latency Tracking:** Monitors server-side inference time down to the millisecond.
  * **Automated CSV Logging:** Every interaction is sanitized and logged for future analysis and model auditing.
  * **Edge Optimized:** Powered by the `Nandi-Mini-150M` model, running efficiently on local GPU or CPU.
  * **Permanent Deployment:** Pre-configured for **ngrok Static Domains** and Basic Authentication.

-----

## 🛠️ Technology Stack

| Component | Technology |
| :--- | :--- |
| **Backend** | Python, Flask, Streamlit |
| **Frontend** | HTML5, CSS3, JavaScript (Marked.js) |
| **Visualization** | Pandas, Plotly Express |
| **AI Engine** | Hugging Face Transformers, PyTorch |
| **Model** | `Rta-AILabs/Nandi-Mini-150M-Instruct` |

-----

## 🚀 Installation

### 1\. Clone the Repository

```bash
git clone https://github.com/arafmustavi/ai-amplify-chat.git
cd ai-amplify-chat
```

### 2\. Install Dependencies

```bash
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118  # For CUDA
pip install flask transformers accelerate streamlit pandas plotly-express
```

### 3\. Project Structure

```text
/ai-amplify-chat
│── app.py                 # Chat Backend (Public)
│── dashboard.py           # Analytics Dashboard (Private)
│── amplify_chat_history.csv # Automated Data Logs
└── /templates
    └── index.html         # Modern Chat UI
```

-----

## 💻 How to Run

### I. The Chat Interface (Public)

Run the Flask server to start the chat:

```bash
python app.py
```

Open: `http://127.0.0.1:5000`

### II. The Admin Dashboard (Private)

Run the Streamlit app in a new terminal to view analytics:

```bash
streamlit run dashboard.py
```

Open: `http://127.0.0.1:8501`

-----

## 🌐 Remote Deployment (ngrok)

To share your AI while keeping your data private, use the following ngrok commands:

1.  **Expose Chat:** `ngrok http --url=your-static-domain.ngrok-free.app 5000`
2.  **Expose Dashboard (with Password):** `ngrok http 8501 --basic-auth="admin:your_secure_password"`

-----

## ⚙️ Model & Data Configuration

  - **Logging:** Data is stored in `amplify_chat_history.csv` with columns: `timestamp`, `prompt`, `response`, `latency_sec`, and `device`.
  - **Formatting:** Supports full GFM (GitHub Flavored Markdown) with auto-newline handling.
  - **Precision:** Uses `bfloat16` for rapid local inference.

-----

*Built with ❤️ for a private, fast, and beautiful AI experience.*