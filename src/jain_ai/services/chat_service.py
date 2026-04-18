import re

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
from .session_service import (
    append_chat_message,
    clear_uploaded_context,
    get_recent_chat_context,
    get_uploaded_context,
    has_uploaded_context,
    save_uploaded_context,
)
from .upload_service import extract_uploaded_text


logger = get_logger("jain_ai.chat_service")


def split_compound_question(user_input):
    normalized = re.sub(r"\s+", " ", (user_input or "").strip())
    if not normalized:
        return []

    parts = re.split(r"\s+(?:and|also)\s+(?=(?:what|which|who|where|when|how)\b)", normalized, flags=re.IGNORECASE)
    cleaned_parts = [part.strip(" ?.") + "?" for part in parts if part.strip()]

    if len(cleaned_parts) <= 1:
        return []

    return cleaned_parts[:2]


def answer_rag_question(query, system_prompt, fallback_prompt, recent_chat_context):
    context_bundle = get_rag_pipeline().build_context_bundle(query)
    return answer_with_fallback(
        query,
        context_bundle["context"],
        system_prompt,
        fallback_prompt,
        chat_context=recent_chat_context,
        source_references=context_bundle["sources"],
    )


def answer_compound_rag_question(user_input, system_prompt, fallback_prompt, recent_chat_context):
    sub_questions = split_compound_question(user_input)
    if not sub_questions:
        return None

    answers = []
    for index, sub_question in enumerate(sub_questions, start=1):
        answer = answer_rag_question(sub_question, system_prompt, fallback_prompt, recent_chat_context)
        answers.append(f"{index}. {sub_question}\n{answer}")

    return "\n\n".join(answers)


def handle_chat_turn(user_input, file):
    uploaded_filename = file.filename if file and file.filename else ""
    user_message = user_input or f"Analyze uploaded file: {uploaded_filename}"
    recent_chat_context = get_recent_chat_context()
    active_uploaded_text, active_uploaded_filename = get_uploaded_context()
    append_chat_message("user", user_message)

    try:
        route = route_request(user_input, uploaded_filename, has_uploaded_context=has_uploaded_context())

        if route == "upload":
            if file and uploaded_filename:
                extracted_text, filename, upload_error = extract_uploaded_text(file)
                if upload_error:
                    clear_uploaded_context()
                    bot_reply = upload_error
                elif not extracted_text or extracted_text == "NO_TEXT_FOUND":
                    clear_uploaded_context()
                    bot_reply = f"I could not extract readable text from `{filename}`."
                else:
                    save_uploaded_context(extracted_text, filename)
                    question = user_input or "Summarize this file."
                    bot_reply = answer_from_context(
                        question,
                        extracted_text[:MAX_CONTEXT_CHARS],
                        FILE_SYSTEM_PROMPT,
                        chat_context=recent_chat_context,
                    )
            else:
                if not active_uploaded_text:
                    bot_reply = "Please upload a PDF or image first so I can answer questions about that file."
                else:
                    question = user_input or f"Summarize `{active_uploaded_filename or 'the uploaded file'}`."
                    bot_reply = answer_from_context(
                        question,
                        active_uploaded_text[:MAX_CONTEXT_CHARS],
                        FILE_SYSTEM_PROMPT,
                        chat_context=recent_chat_context,
                    )
        elif route == "summarize":
            bot_reply = answer_rag_question(
                user_input or "Summarize the relevant content.",
                SUMMARIZATION_SYSTEM_PROMPT,
                NO_CONTEXT_FALLBACK_PROMPT,
                recent_chat_context,
            )
        elif route == "rag":
            bot_reply = answer_compound_rag_question(
                user_input,
                RAG_SYSTEM_PROMPT,
                NO_CONTEXT_FALLBACK_PROMPT,
                recent_chat_context,
            ) or answer_rag_question(
                user_input,
                RAG_SYSTEM_PROMPT,
                NO_CONTEXT_FALLBACK_PROMPT,
                recent_chat_context,
            )
        elif route == "follow_up":
            bot_reply = answer_rag_question(
                user_input,
                FOLLOW_UP_SYSTEM_PROMPT,
                GENERAL_SYSTEM_PROMPT,
                recent_chat_context,
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
