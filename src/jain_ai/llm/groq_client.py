import base64
import os

from groq import Groq

from ..constants.settings import TEXT_MODEL, VISION_MODEL


_client = None
_cached_api_key = None


def reset_client():
    global _client, _cached_api_key
    _client = None
    _cached_api_key = None


def get_groq_client():
    global _client, _cached_api_key
    from ..config import BASE_DIR
    from ..utils.file_utils import load_local_env

    # Reload local .env so newly added or rotated keys are picked up without requiring server restart
    env_path = os.path.join(BASE_DIR, ".env")
    if os.path.exists(env_path):
        load_local_env(env_path)

    api_key = os.environ.get("GROQ_API_KEY")
    if not api_key:
        _client = None
        _cached_api_key = None
        raise RuntimeError("GROQ_API_KEY is not set.")

    if _client is None or api_key != _cached_api_key:
        _client = Groq(api_key=api_key, timeout=30.0, max_retries=1)
        _cached_api_key = api_key

    return _client


def call_text_model(system_prompt, user_prompt, temperature=0.1):
    response = get_groq_client().chat.completions.create(
        model=TEXT_MODEL,
        temperature=temperature,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
    )
    return response.choices[0].message.content


def image_bytes_to_data_url(image_bytes, mime_type):
    encoded = base64.b64encode(image_bytes).decode("utf-8")
    return f"data:{mime_type};base64,{encoded}"


def run_vision_ocr(image_bytes, mime_type):
    response = get_groq_client().chat.completions.create(
        model=VISION_MODEL,
        temperature=0.0,
        messages=[
            {
                "role": "system",
                "content": (
                    "Extract all readable text from the image exactly as it appears. "
                    "Return plain text only. If no text is visible, say 'NO_TEXT_FOUND'."
                ),
            },
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": "Extract the text from this image."},
                    {
                        "type": "image_url",
                        "image_url": {"url": image_bytes_to_data_url(image_bytes, mime_type)},
                    },
                ],
            },
        ],
    )
    return response.choices[0].message.content.strip()
