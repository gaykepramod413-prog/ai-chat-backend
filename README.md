# 🤖 AI Chat Backend

<div align="center">

**A lightweight Flask API that connects a chat client to an AI model through the Groq API.**

![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=flat-square&logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-3.0-000000?style=flat-square&logo=flask&logoColor=white)
![API](https://img.shields.io/badge/API-REST-0A7EA4?style=flat-square)

</div>

## ✨ Features

- Flask-based REST API with CORS enabled.
- Sends user messages to the Groq chat-completions endpoint.
- Uses the `openai/gpt-oss-120b` model configured in `server.py`.
- JSON responses with basic request validation and error handling.
- Reads the Groq API key from an environment variable.

## 🧱 Tech Stack

- Python
- Flask and Flask-CORS
- Requests
- Groq API (OpenAI-compatible chat completions endpoint)
- Gunicorn for production serving

## 📁 Project Structure

```text
ai-chat-backend/
├── server.py
├── requirements.txt
└── README.md
```

## ⚙️ Run Locally

1. Clone the repository:

   ```bash
   git clone https://github.com/gaykepramod413-prog/ai-chat-backend.git
   cd ai-chat-backend
   ```

2. Create and activate a virtual environment:

   ```bash
   python -m venv .venv
   # Windows
   .venv\Scripts\activate
   # macOS / Linux
   source .venv/bin/activate
   ```

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Set your API key:

   **Windows PowerShell**
   ```powershell
   $env:GROQ_API_KEY = "YOUR_GROQ_API_KEY"
   ```

   **macOS / Linux**
   ```bash
   export GROQ_API_KEY="YOUR_GROQ_API_KEY"
   ```

5. Start the server:

   ```bash
   python server.py
   ```

   The default local port is `10000` (or the value provided by `PORT`).

## 🔌 API

### Health check

`GET /`

Example response:

```json
{
  "status": "AI Backend Running Successfully 🚀"
}
```

### Send a chat message

`POST /chat`

Request:

```json
{
  "message": "Explain machine learning in simple words."
}
```

Successful response:

```json
{
  "response": "AI-generated reply..."
}
```

Example with cURL:

```bash
curl -X POST http://localhost:10000/chat \
  -H "Content-Type: application/json" \
  -d '{"message":"Hello! Explain Python briefly."}'
```

## 🚀 Deployment

For a WSGI deployment, the application can be served with:

```bash
gunicorn server:app
```

Configure `GROQ_API_KEY` and the platform-provided `PORT` as environment variables. Never commit API keys or other secrets to the repository.

## 🗺️ Next Improvements

- Add automated tests for API success and failure cases.
- Add request-size limits, rate limiting, and structured logging.
- Add conversation history when the client requires multi-turn context.
- Add a configurable model name through environment variables.

---

<div align="center">

**Built by [Pramod Gayke](https://github.com/gaykepramod413-prog)**

</div>
