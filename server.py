from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import os

app = Flask(__name__)
CORS(app)

# Get API key from Render environment
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")

# Groq endpoint
GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"


@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "status": "AI Backend Running Successfully 🚀"
    })


@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()

    if not data:
        return jsonify({"error": "No JSON received"}), 400

    user_message = data.get("message")

    if not user_message:
        return jsonify({"error": "Message field is required"}), 400

    if not GROQ_API_KEY:
        return jsonify({"error": "GROQ_API_KEY not configured"}), 500

    try:
        headers = {
            "Authorization": f"Bearer {GROQ_API_KEY}",
            "Content-Type": "application/json"
        }

        payload = {
            "model": "llama3-8b-8192",
            "messages": [
                {
                    "role": "system",
                    "content": "You are a helpful AI assistant."
                },
                {
                    "role": "user",
                    "content": user_message
                }
            ],
            "temperature": 0.7,
            "max_tokens": 1024
        }

        response = requests.post(
            GROQ_URL,
            headers=headers,
            json=payload,
            timeout=30
        )

        # If Groq returns error, show full response
        if response.status_code != 200:
            return jsonify({
                "error": "Groq API Error",
                "details": response.text
            }), response.status_code

        result = response.json()

        ai_reply = result["choices"][0]["message"]["content"]

        return jsonify({"response": ai_reply})

    except requests.exceptions.Timeout:
        return jsonify({"error": "Groq request timed out"}), 500

    except requests.exceptions.RequestException as e:
        return jsonify({"error": f"Request error: {str(e)}"}), 500

    except Exception as e:
        return jsonify({"error": f"Server error: {str(e)}"}), 500


# For local testing only (Render uses Gunicorn)
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
