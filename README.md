# Jain AI

Flask-based academic assistant with:

- RAG over local Jain University PDFs
- OCR for images and PDFs
- session-isolated chat per browser/device
- upload-aware routing for `general`, `rag`, and `upload`
- scalable package structure for future multi-developer work

## Project structure

```text
jain-ai/
├── .env
├── .env.example
├── pyproject.toml
├── uv.lock
├── README.md
├── alembic.ini
├── app.py
├── wsgi.py
├── scripts/
├── docs/
├── tests/
├── data/
│   ├── raw/
│   │   └── academics/
│   ├── processed/
│   └── uploads/
├── storage/
│   ├── vector_db/
│   ├── logs/
│   └── cache/
├── templates/
│   └── index.html
├── static/
│   ├── css/
│   ├── js/
│   ├── images/
│   └── icons/
└── src/
    └── jain_ai/
        ├── routes/
        ├── services/
        ├── rag/
        ├── ocr/
        ├── llm/
        ├── db/
        ├── schemas/
        ├── utils/
        └── constants/
```

## Run locally

```bash
uv sync
uv run app.py
```

## Useful commands

```bash
uv run app.py
uv run python scripts/verify_setup.py
uv run python scripts/index_data.py
uv run pytest
```

## Key paths

- PDFs: `data/raw/academics/`
- Chroma store: `storage/vector_db/`
- HTML template: `templates/index.html`
- Flask entrypoint: `app.py`
- Production WSGI entrypoint: `wsgi.py`

## Environment variables

`.env` is loaded automatically.

- `FLASK_SECRET_KEY`
- `OPENAI_API_KEY`
- `GROQ_API_KEY`
- `HOST`
- `PORT`
- `LOG_LEVEL`
- `SESSION_COOKIE_SECURE`
