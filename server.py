from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import os

app = Flask(__name__)
CORS(app)

# Get API Key safely
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")

GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"


@app.route("/", methods=["GET"])
def home():
    return jsonify({"status": "Groq AI Backend Running"})


def get_ai_response(prompt):
    if not GROQ_API_KEY:
        return "Server Error: GROQ_API_KEY is not configured."

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

        response = requests.post(
            GROQ_URL,
            headers=headers,
            json=payload,
            timeout=30
        )

        response.raise_for_status()  # Raises error if status != 200

        result = response.json()

        return result.get("choices", [{}])[0].get("message", {}).get("content", "No response from AI")

    except requests.exceptions.RequestException as e:
        return f"Request Error: {str(e)}"
    except Exception as e:
        return f"Server Error: {str(e)}"


@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()

    if not data or "message" not in data:
        return jsonify({"error": "Message is required"}), 400

    ai_reply = get_ai_response(data["message"])
    return jsonify({"response": ai_reply})


# IMPORTANT: Run server
if __name__ == "__main__":
    app.run(debug=True)
