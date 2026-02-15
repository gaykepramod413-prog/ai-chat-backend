from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import os
import time

server = Flask(__name__)
CORS(server)

# ==============================
# HuggingFace Config
# ==============================
HF_API_URL = "https://api-inference.huggingface.co/models/microsoft/DialoGPT-small"
HF_API_KEY = os.environ.get("HF_API_KEY")

if not HF_API_KEY:
    raise ValueError("HF_API_KEY is not set in environment variables")

headers = {
    "Authorization": f"Bearer {HF_API_KEY}"
}

# ==============================
# Health Check Route
# ==============================
@server.route("/", methods=["GET"])
def home():
    return jsonify({"status": "Backend Running Successfully 🚀"})

# ==============================
# AI Response Function (Upgraded)
# ==============================
def get_ai_response(prompt):
    try:
        payload = {"inputs": prompt}

        response = requests.post(
            HF_API_URL,
            headers=headers,
            json=payload,
            timeout=60
        )

        result = response.json()

        # If model is loading → wait & retry once
        if isinstance(result, dict) and "error" in result:
            if "loading" in result["error"].lower():
                time.sleep(20)

                response = requests.post(
                    HF_API_URL,
                    headers=headers,
                    json=payload,
                    timeout=60
                )
                result = response.json()

        # Successful response
        if isinstance(result, list):
            return result[0].get("generated_text", "No response generated.")

        # Still error after retry
        if isinstance(result, dict) and "error" in result:
            return "AI is warming up. Please try again."

        return "Unexpected response from AI."

    except requests.exceptions.Timeout:
        return "Request timed out. Please try again."
    except Exception as e:
        return f"Server error: {str(e)}"

# ==============================
# Chat Endpoint
# ==============================
@server.route("/chat", methods=["POST"])
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
