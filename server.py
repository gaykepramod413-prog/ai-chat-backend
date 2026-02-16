from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import os

app = Flask(__name__)
CORS(app)

# Get Groq API key from Render Environment Variables
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")

GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"


@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "status": "AI Backend Running Successfully 🚀"
    })


def get_ai_response(user_message):
    if not GROQ_API_KEY:
        return "Server configuration error: API key missing."

    try:
        headers = {
            "Authorization": f"Bearer {GROQ_API_KEY}",
            "Content-Type": "application/json"
        }

        payload = {
            "model": "llama3-8b-8192",
            "messages": [
                {"role": "system", "content": "You are a helpful AI assistant."},
                {"role": "user", "content": user_message}
            ]
        }

        response = requests.post(
            GROQ_URL,
            headers=headers,
            json=payload,
            timeout=30
        )

        response.raise_for_status()
        result = response.json()

        return result["choices"][0]["message"]["content"]

    except requests.exceptions.RequestException as e:
        return f"Request Error: {str(e)}"
    except Exception as e:
        return f"Server Error: {str(e)}"


@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()

    if not data or "message" not in data:
        return jsonify({"error": "Message field is required"}), 400

    user_message = data["message"]
    ai_reply = get_ai_response(user_message)

    return jsonify({
        "response": ai_reply
    })


# Required for Render
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
