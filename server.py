from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import os

app = Flask(__name__)
CORS(app)

# ==============================
# Groq Config
# ==============================
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")

if not GROQ_API_KEY:
    raise ValueError("GROQ_API_KEY is not set in environment variables")

GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"

# ==============================
# Health Check
# ==============================
@app.route("/", methods=["GET"])
def home():
    return jsonify({"status": "Groq AI Backend Running 🚀"})

# ==============================
# AI Function (Groq)
# ==============================
def get_ai_response(prompt):
    try:
        headers = {
            "Authorization": f"Bearer {GROQ_API_KEY}",
            "Content-Type": "application/json"
        }

        payload = {
            "model": "llama3-8b-8192",
            "messages": [
                {"role": "system", "content": "You are a helpful AI assistant."},
                {"role": "user", "content": prompt}
            ]
        }

        response = requests.post(GROQ_URL, headers=headers, json=payload)

        result = response.json()

        return result["choices"][0]["message"]["content"]

    except Exception as e:
        return f"Error: {str(e)}"

# ==============================
# Chat Endpoint
# ==============================
@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()

    if not data or "message" not in data:
        return jsonify({"error": "Message is required"}), 400

    user_message = data["message"]
    ai_reply = get_ai_response(user_message)

    return jsonify({"response": ai_reply})

# ==============================
# Run App (Render Compatible)
# ==============================
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
