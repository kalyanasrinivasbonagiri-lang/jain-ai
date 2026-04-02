# Jain AI

Jain AI is a modular Flask application for academic assistance, document question-answering, and upload-aware chat. It combines retrieval-augmented generation (RAG), OCR, and session-based conversation flows to support questions grounded in local university documents and uploaded files.

## Highlights

- Modular Flask app built with an application factory
- Retrieval over local PDF content using Chroma and OpenAI embeddings
- OCR support for PDFs and images
- Session-isolated chat history per browser session
- Web routes, health endpoint, and API/admin blueprints
- Organized project structure for iterative team development

## Architecture Overview

The application is split into focused packages under `src/jain_ai`:

- `rag/` handles document loading, chunking, indexing, retrieval, and route registration
- `ocr/` handles text extraction from uploaded PDFs and images
- `llm/` handles Groq client setup and model calls
- `services/` contains chat, routing, upload, and session logic
- `schemas/` contains request/response data structures
- `db/` contains persistence-oriented modules for future expansion
- `utils/` contains shared helpers for files, logging, validation, and security

## Project Structure

```text
jain-ai/
├── app.py
├── wsgi.py
├── pyproject.toml
├── README.md
├── .env.example
├── data/
│   ├── raw/academics/
│   ├── processed/
│   └── uploads/
├── storage/
│   ├── vector_db/
│   ├── logs/
│   └── cache/
├── docs/
├── scripts/
├── static/
├── templates/
└── src/jain_ai/
    ├── app_factory.py
    ├── config.py
    ├── constants/
    ├── db/
    ├── llm/
    ├── ocr/
    ├── rag/
    ├── schemas/
    ├── services/
    └── utils/
```

## Requirements

- Python 3.11+
- `uv` recommended for dependency management
- Groq API key for chat and OCR-backed responses
- OpenAI API key for embedding-based retrieval

## Installation

```bash
uv sync
```

If you prefer a virtual environment manually:

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -e .
```

## Environment Configuration

Create a local `.env` file based on `.env.example`.

Example variables:

```env
GROQ_API_KEY=your-groq-api-key
OPENAI_API_KEY=your-openai-api-key
FLASK_SECRET_KEY=replace-with-a-long-random-secret
HOST=0.0.0.0
PORT=5000
LOG_LEVEL=INFO
SESSION_COOKIE_SECURE=false
```

Notes:

- `GROQ_API_KEY` is required for model responses and OCR-assisted extraction
- `OPENAI_API_KEY` is required for embedding-based vector retrieval
- If `OPENAI_API_KEY` is missing, RAG may fall back to reduced functionality depending on the code path

## Running the App

Start the development server:

```bash
uv run app.py
```

If `uv` has a local cache permission issue on Windows, run the app with the virtual environment Python instead:

```bash
.\.venv\Scripts\python.exe app.py
```

The app reads host and port from the environment and defaults to:

- Host: `0.0.0.0`
- Port: `5000`

## WSGI Entrypoint

For production-style hosting, use:

```python
wsgi:app
```

The WSGI entrypoint is defined in `wsgi.py`.

## Data Layout

Place source academic PDFs in:

```text
data/raw/academics/
```

Runtime-generated directories:

- `data/uploads/` for uploaded user files
- `data/processed/` for processed outputs
- `storage/vector_db/` for Chroma persistence
- `storage/logs/` for application logs
- `storage/cache/` for temporary cached data

## Available Routes

- `/` main chat interface
- `/health` application health and vector-store readiness
- `/api/ping` simple API status check
- `/admin/status` admin readiness check

## Useful Commands

Run setup verification:

```bash
uv run python scripts/verify_setup.py
```

Index or reindex document data:

```bash
uv run python scripts/index_data.py
uv run python scripts/reindex_documents.py
```

Seed or prepare local data:

```bash
uv run python scripts/seed_data.py
```

Run tests:

```bash
uv run pytest
```

## Testing

The test suite lives under `tests/` and includes coverage for:

- OCR flows
- RAG behavior
- route handling
- uploads
- session behavior

## Development Notes

- The app uses an application factory in `src/jain_ai/app_factory.py`
- Session chat history is stored in Flask session state
- The health endpoint initializes the RAG pipeline and reports document/vector readiness
- The project is structured to support future extraction of services, routes, and persistence layers

## Security Notes

- Never commit real API keys or secrets
- Keep `.env` local and untracked
- Use a strong `FLASK_SECRET_KEY` outside local development
- Set `SESSION_COOKIE_SECURE=true` when running behind HTTPS

## Repository Documentation

Additional technical documentation is available in:

- `docs/api.md`
- `docs/architecture.md`
- `docs/deployment.md`
- `docs/rag_pipeline.md`

## License

Add your preferred license information here before public distribution.
