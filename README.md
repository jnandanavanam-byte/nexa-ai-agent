<div align="center">

# ✨ Nexa AI Agent

### A local, multi-agent assistant for chat, data, property search, and voice

**Ask questions in plain language. Let specialized agents route, reason, and respond.**

<br>

![Python](https://img.shields.io/badge/Python-3.11%2B-3776AB?logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/API-FastAPI-009688?logo=fastapi&logoColor=white)
![Database](https://img.shields.io/badge/Database-SQLite-003B57?logo=sqlite&logoColor=white)
![Inference](https://img.shields.io/badge/LLM-Ollama-black?logo=ollama&logoColor=white)

</div>

---

## 📌 About

**Nexa AI Agent** is a FastAPI backend that routes requests to focused agents for natural-language SQL, real-estate search, and general conversation. It runs its language model locally through **Ollama**, stores sample business data in **SQLite**, and includes speech-to-text and text-to-speech endpoints.

The project is intended as a learning and development project. Real-estate scraping depends on Firecrawl and supported listing pages; sample listings are used as a fallback.

## 🌟 Features

- 🧭 **Intent routing** — classifies requests as SQL, real estate, or general chat.
- 🗃️ **Text-to-SQL** — generates read-only queries using the discovered SQLite schema.
- 🏠 **Property search** — extracts search criteria, filters listings, and can scrape supported locations.
- 🎙️ **Voice input** — transcribes uploaded audio locally with Whisper.
- 🔊 **Voice output** — generates WAV speech using `pyttsx3`.
- 💬 **Short-term chat memory** — keeps a small in-memory history for general conversation.
- 📖 **Interactive API docs** — explore and call endpoints in Swagger UI.

## 🧱 Architecture

```text
Text or audio request
          │
          ▼
    FastAPI API layer
       ┌──┴───────────────┐
       ▼                  ▼
  Intent router       Voice pipeline
       │          Whisper → chat → TTS
   ┌───┼───────────┐
   ▼   ▼           ▼
 SQL  Property   General chat
 agent  agent     + memory
   │     │           │
SQLite  Firecrawl   Ollama
        / samples   (Gemma 4 E4B)
```

## 🛠️ Technology

| Area | Technologies |
| --- | --- |
| API | FastAPI, Uvicorn, Pydantic |
| Language model | Ollama, `gemma4:e4b` |
| Data and SQL | SQLite, SQLAlchemy |
| Speech | OpenAI Whisper (`base` model), `pyttsx3` |
| Property listings | Firecrawl with local sample-listing fallback |

## ✅ Prerequisites

- **Python 3.11 or newer**
- **Ollama** installed and running locally
- The Ollama model used by the app: `gemma4:e4b`
- **FFmpeg** installed and available on `PATH` for Whisper audio processing
- A **Firecrawl API key** only if you want to try live property-page scraping

> The chat and SQL agents use Ollama locally. Live property scraping is an optional external service and requires network access and a Firecrawl key.

## 🚀 Quick start (Windows PowerShell)

Run these commands from the project root:

```powershell
cd backend
py -3.11 -m venv ..\venv
..\venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
```

Pull the model and make sure Ollama is running:

```powershell
ollama pull gemma4:e4b
ollama serve
```

If Ollama is already running as a background service, you only need the `ollama pull` command. Keep Ollama running. In a **second** PowerShell terminal opened at the project root, start the API:

```powershell
cd backend
..\venv\Scripts\Activate.ps1
python -m uvicorn app.main:app --reload
```

Open the interactive API documentation:

**http://127.0.0.1:8000/docs**

The SQLite database is located at `backend/app/data/sales.db`. The app creates its tables from the SQLAlchemy schema when the database initialization module is run:

```powershell
python -m app.core.db_init
```

To insert the included sample customers, products, and orders, run this once against a fresh or empty database:

```powershell
python -m app.core.db_seed
```

> The seed script inserts fixed IDs and is not designed to be run repeatedly against an already seeded database.

### Optional: enable live property scraping

Set the Firecrawl key in the same PowerShell session before starting Uvicorn:

```powershell
$env:FIRECRAWL_API_KEY = "your-firecrawl-api-key"
```

The current scraper has configured pages for **Dubai** and **Abu Dhabi**. If scraping is unavailable or returns no listings, the property agent falls back to its bundled sample listings.

## 🔌 API endpoints

### `GET /`

Simple service health response.

### `POST /chat`

Routes a text message to the SQL, real-estate, or general-chat agent.

**Request**

```json
{
  "message": "Show customers from Hyderabad"
}
```

The response shape depends on the selected agent. SQL responses include generated SQL and query results; general-chat responses include an `agent` and `response`.

### `POST /voice`

Accepts an audio upload as multipart form data in the `file` field. The endpoint transcribes the audio, routes the recognized text through chat, and returns the recognized text, selected agent, and generated audio file path.

Use the Swagger UI to try this endpoint and upload a supported audio file.

## 🗂️ Project layout

```text
Nexa-AI-Agent/
├── README.md
├── backend/
│   ├── requirements.txt
│   └── app/
│       ├── main.py
│       ├── agents/       # Intent, SQL, and property agents
│       ├── api/          # Chat and voice routes
│       ├── core/         # Ollama, memory, and SQLite setup
│       ├── data/         # Listing helpers and SQLite database
│       └── voice/        # Speech-to-text and text-to-speech
└── venv/                 # Local virtual environment (created during setup)
```

## 🧠 Notes and limitations

- Conversation history is held **in process memory**, is shared by requests to that running process, and is cleared when the process restarts.
- The project uses a local Ollama model; the first model download can take time and disk space.
- The SQL agent is intended for read-only, local sample-data queries. Do not expose this development API publicly without adding appropriate authentication, validation, and deployment safeguards.
- Property scraping is limited to the locations configured in the scraper; bundled examples provide a fallback, not guaranteed live market data.
- Voice processing requires the speech dependencies and FFmpeg listed above. Audio output paths are local paths, not public download URLs.
- The SQLite database and generated audio files are local runtime data and should not be committed.

## 🔐 Secrets

Do not commit API keys, passwords, or other credentials. Keep optional service keys out of source control and rotate any key that may have been exposed.

## 📄 License

No license file is currently included. Add a `LICENSE` file before redistributing this project under specific license terms.

---

<div align="center">

**Built for learning, experimentation, and local AI workflows.** 🚀

</div>
