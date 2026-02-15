from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import os

app = Flask(__name__)
CORS(app)

GROQ_API_KEY = os.environ.get("GROQ_API_KEY")

if not GROQ_API_KEY:
    raise ValueError("GROQ_API_KEY is not set in environment variables")

GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"

@app.route("/", methods=["GET"])
def home():
    return jsonify({"status": "Groq AI Backend Running 🚀"})

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

        if response.status_code != 200:
            return f"Groq Error: {response.text}"

        result = response.json()

        if "choices" in result:
            return result["choices"][0]["message"]["content"]

        return f"Unexpected response: {result}"

    except Exception as e:
        return f"Server Error: {str(e)}"

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()

    if not data or "message" not in data:
        return jsonify({"error": "Message is required"}), 400

    ai_reply = get_ai_response(data["message"])
    return jsonify({"response": ai_reply})
