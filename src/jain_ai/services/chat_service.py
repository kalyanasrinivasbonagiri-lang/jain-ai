from groq import APIConnectionError, APIError, APITimeoutError

from ..constants.prompts import (
    FILE_SYSTEM_PROMPT,
    FOLLOW_UP_SYSTEM_PROMPT,
    GENERAL_SYSTEM_PROMPT,
    NO_CONTEXT_FALLBACK_PROMPT,
    RAG_SYSTEM_PROMPT,
    SUMMARIZATION_SYSTEM_PROMPT,
)
from ..constants.settings import MAX_CONTEXT_CHARS
from ..llm.groq_client import call_text_model
from ..rag.pipeline import get_rag_pipeline
from ..utils.logging_utils import get_logger
from .response_service import answer_from_context, answer_with_fallback
from .routing_service import route_request
from .session_service import append_chat_message, get_recent_chat_context
from .upload_service import extract_uploaded_text


logger = get_logger("jain_ai.chat_service")


def handle_chat_turn(user_input, file):
    uploaded_filename = file.filename if file and file.filename else ""
    user_message = user_input or f"Analyze uploaded file: {uploaded_filename}"
    recent_chat_context = get_recent_chat_context()
    append_chat_message("user", user_message)

    try:
        route = route_request(user_input, uploaded_filename)

        if route == "upload":
            extracted_text, filename, upload_error = extract_uploaded_text(file)
            if upload_error:
                bot_reply = upload_error
            elif not extracted_text or extracted_text == "NO_TEXT_FOUND":
                bot_reply = f"I could not extract readable text from `{filename}`."
            else:
                question = user_input or "Summarize this file."
                bot_reply = answer_from_context(
                    question,
                    extracted_text[:MAX_CONTEXT_CHARS],
                    FILE_SYSTEM_PROMPT,
                    chat_context=recent_chat_context,
                )
        elif route == "summarize":
            context = get_rag_pipeline().build_context(user_input)
            bot_reply = answer_with_fallback(
                user_input or "Summarize the relevant content.",
                context,
                SUMMARIZATION_SYSTEM_PROMPT,
                NO_CONTEXT_FALLBACK_PROMPT,
                chat_context=recent_chat_context,
            )
        elif route == "rag":
            context = get_rag_pipeline().build_context(user_input)
            bot_reply = answer_with_fallback(
                user_input,
                context,
                RAG_SYSTEM_PROMPT,
                NO_CONTEXT_FALLBACK_PROMPT,
                chat_context=recent_chat_context,
            )
        elif route == "follow_up":
            context = get_rag_pipeline().build_context(user_input)
            bot_reply = answer_with_fallback(
                user_input,
                context,
                FOLLOW_UP_SYSTEM_PROMPT,
                GENERAL_SYSTEM_PROMPT,
                chat_context=recent_chat_context,
            )
        else:
            general_prompt = user_input
            if recent_chat_context:
                general_prompt = (
                    f"Recent conversation:\n{recent_chat_context}\n\n"
                    f"Current user message:\n{user_input}\n\n"
                    "Use the recent conversation only when it helps resolve follow-up references."
                )
            bot_reply = call_text_model(GENERAL_SYSTEM_PROMPT, general_prompt, temperature=0.2)
    except RuntimeError as exc:
        logger.warning("Model configuration issue: %s", exc)
        bot_reply = (
            "The AI service is not configured yet. Please check your API keys in the `.env` file "
            "and try again."
        )
    except (APIConnectionError, APITimeoutError) as exc:
        logger.warning("AI service connection issue: %s", exc)
        bot_reply = (
            "I couldn't reach the AI service right now. Please check your internet connection, DNS, "
            "or firewall settings and try again."
        )
    except APIError as exc:
        logger.warning("AI service request failed: %s", exc)
        bot_reply = (
            "The AI service returned an error while processing your request. Please try again in a moment."
        )
    except Exception as exc:
        logger.exception("Request handling failed: %s", exc)
        bot_reply = (
            "I ran into a temporary problem while processing that request. "
            "Please try again in a moment."
        )

    append_chat_message("bot", bot_reply)
    return bot_reply
