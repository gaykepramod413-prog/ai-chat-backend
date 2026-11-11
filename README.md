# 🤖 AI Chat Backend

<div align="center">

**A lightweight Flask REST API that connects a chat client to an AI model through the Groq API.**

![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=flat-square&logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-3.0-000000?style=flat-square&logo=flask&logoColor=white)
![API](https://img.shields.io/badge/API-REST-0A7EA4?style=flat-square)
![License](https://img.shields.io/badge/Status-Portfolio%20Project-blue?style=flat-square)

</div>

## Overview

This project provides a simple backend for an AI chat application. A client sends a message to the Flask API, the backend validates the request, securely loads its Groq API key from an environment variable, calls the Groq chat-completions endpoint, and returns the generated answer as JSON.

## Features

- Flask-based REST API with CORS enabled.
- JSON request validation and clear error responses.
- Integration with the Groq OpenAI-compatible chat-completions endpoint.
- Configured model: `openai/gpt-oss-120b`.
- Server-side API key configuration using `GROQ_API_KEY`.
- Request timeout and exception handling.
- Gunicorn-compatible deployment.

## Tech Stack

- **Language:** Python 3.10+
- **Backend:** Flask, Flask-CORS
- **HTTP client:** Requests
- **AI provider:** Groq API
- **Deployment:** Gunicorn

## Architecture & Request Flow

```text
Chat Client
    |
    | POST /chat (JSON: { "message": "..." })
    v
Flask API
    |
    | Validate JSON and message
    | Read GROQ_API_KEY from server environment
    v
Groq Chat Completions API
    |
    | Authorization: Bearer <API_KEY>
    | Model: openai/gpt-oss-120b
    v
AI-generated completion
    |
    v
Flask returns { "response": "..." }
```

### Request lifecycle

1. The client sends a `POST /chat` request with a JSON message.
2. Flask checks that JSON and the `message` field are present.
3. The backend checks that `GROQ_API_KEY` is configured.
4. The server sends the message to Groq with a Bearer authorization header.
5. The backend checks the provider response and extracts the generated text.
6. Flask returns the answer to the client as JSON.

## Authentication & Credential Handling

**Current implementation:** this project authenticates the backend to Groq using a provider API key. It does **not** currently implement end-user login, JWT issuance, refresh tokens, or session management.

- The key is read with `os.environ.get("GROQ_API_KEY")`.
- The key is attached to the outbound Groq request in the `Authorization: Bearer ...` header.
- The key should remain on the server and must never be placed in frontend code or committed to Git.
- Use HTTPS for deployed traffic and keep the key in the hosting provider's secret/environment configuration.
- Rotate the key immediately if it is exposed.

## Project Structure

```text
ai-chat-backend/
├── server.py
├── requirements.txt
└── README.md
```

## Run Locally

1. Clone the repository:

   ```bash
   git clone https://github.com/gaykepramod413-prog/ai-chat-backend.git
   cd ai-chat-backend
   ```

2. Create and activate a virtual environment:

   ```bash
   python -m venv .venv
   # Windows PowerShell
   .venv\Scripts\Activate.ps1
   # macOS / Linux
   source .venv/bin/activate
   ```

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Configure the API key.

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

The default local port is `10000`, or the value supplied through `PORT`.

## API Reference

### Health check

`GET /`

Example response:

```json
{
  "status": "AI Backend Running Successfully 🚀"
}
```

### Chat completion

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

Example:

```bash
curl -X POST http://localhost:10000/chat \
  -H "Content-Type: application/json" \
  -d '{"message":"Explain Python briefly."}'
```

## Error Handling

| Situation | Current behavior |
|---|---|
| Missing JSON body | Returns HTTP 400 |
| Missing message | Returns HTTP 400 |
| Missing Groq API key | Returns HTTP 500 |
| Provider returns non-200 | Returns provider status code |
| Provider timeout | Returns a timeout error |
| Request exception | Returns a request error |

## Deployment

For a WSGI deployment:

```bash
gunicorn server:app
```

Configure `GROQ_API_KEY` and the platform-provided `PORT` as environment variables. Never commit secrets.

## Roadmap

- Add user authentication and authorization (for example, JWT with secure password hashing).
- Add request-size limits, rate limiting, and input-length validation.
- Add automated tests for successful requests and failure cases.
- Return sanitized public error messages and log diagnostic details server-side.
- Add conversation history when multi-turn context is required.
- Make the model configurable through an environment variable.
- Add structured logging and monitoring.

## Interview Notes

**How does authentication work in this project?**

The backend uses a Groq API key to authenticate its server-to-provider request. It reads the key from an environment variable and sends it using the HTTP Bearer authorization scheme. End-user authentication with JWT or sessions is not part of the current implementation.

**Why use environment variables?**

They keep deployment-specific configuration and secrets outside the source code, reducing the risk of accidentally committing credentials.

---

<div align="center">

**Built by [Pramod Gayke](https://github.com/gaykepramod413-prog)**

</div>
