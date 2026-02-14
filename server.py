from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

HF_API_URL = "https://api-inference.huggingface.co/models/microsoft/DialoGPT-medium"
HF_API_KEY = os.environ.get("HF_API_KEY")

headers = {
    "Authorization": f"Bearer {HF_API_KEY}"
}

def get_ai_response(prompt):
    try:
        payload = {"inputs": prompt}

        response = requests.post(
            HF_API_URL,
            headers=headers,
            json=payload,
            timeout=30
        )

        result = response.json()

        if isinstance(result, list):
            return result[0].get("generated_text", "No response")
        else:
            return "Model loading, try again."

    except Exception as e:
        return str(e)

@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    user_message = data.get("message", "")
    ai_reply = get_ai_response(user_message)
    return jsonify({"response": ai_reply})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
