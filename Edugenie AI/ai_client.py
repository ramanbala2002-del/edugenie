import json
import os
import re
import time

from dotenv import load_dotenv
from google import genai

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    raise RuntimeError(
        "GEMINI_API_KEY is not configured. "
        "Please add it to your .env file."
    )

client = genai.Client(api_key=API_KEY)

MODEL_NAME = "gemini-3.5-flash-lite"


def get_model() -> str:
    return MODEL_NAME


def generate_text(
    prompt: str,
    temperature: float = 0.7
) -> str:

    if not prompt or not prompt.strip():
        raise ValueError("Prompt cannot be empty.")

    for attempt in range(3):
        try:
            response = client.models.generate_content(
                model=get_model(),
                contents=prompt,
                config={
                    "temperature": temperature
                }
            )

            response_text = getattr(response, "text", None)

            if not response_text:
                raise RuntimeError(
                    "Gemini returned an empty response."
                )

            return response_text.strip()

        except Exception as error:
            error_text = str(error)

            # Do NOT retry quota errors
            if "429" in error_text or "RESOURCE_EXHAUSTED" in error_text:
                raise RuntimeError(
                    "Gemini API quota has been exceeded. "
                    "Please wait for the quota to reset."
                ) from error

            if "503" in error_text or "UNAVAILABLE" in error_text:
                if attempt < 2:
                    wait_seconds = 2 ** attempt
                    print(
                        f"Gemini temporarily unavailable. "
                        f"Retrying in {wait_seconds} seconds..."
                    )
                    time.sleep(wait_seconds)
                    continue

            raise


def parse_json_response(response_text: str):
    if not response_text:
        return None

    text = response_text.strip()

    text = re.sub(
        r"^```(?:json)?\s*",
        "",
        text,
        flags=re.IGNORECASE
    )

    text = re.sub(
        r"\s*```$",
        "",
        text
    )

    text = text.strip()

    try:
        return json.loads(text)

    except json.JSONDecodeError:
        pass

    object_match = re.search(
        r"\{.*\}",
        text,
        flags=re.DOTALL
    )

    if object_match:
        try:
            return json.loads(object_match.group(0))
        except json.JSONDecodeError:
            pass

    array_match = re.search(
        r"\[.*\]",
        text,
        flags=re.DOTALL
    )

    if array_match:
        try:
            return json.loads(array_match.group(0))
        except json.JSONDecodeError:
            pass

    return None