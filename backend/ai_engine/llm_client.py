# llm_client.py
# Real AI integration using Groq (fast + free-tier LLM inference)
#
# get_ai_review() ek hi API call mein 3 cheezein maangta hai:
#   1. suggestions   -> code improvement tips
#   2. explanation   -> line-by-line style explanation
#   3. error_fix     -> agar error hai to uska problem/reason/fix
#
# Agar GROQ_API_KEY missing hai, ya API call fail ho jaye (network,
# rate limit, invalid JSON, etc.) -> function None return karta hai.
# compiler_engine.py isi None ko dekh kar purane rule-based system
# (suggestion.py / explanation.py / error_ai.py) par fallback kar leta hai.
# Matlab app KABHI crash nahi hoga, chahe AI down ho ya key hi na ho.

import os
import json
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.environ.get("GROQ_API_KEY")

# Groq ka current fast + free-tier friendly model
MODEL_NAME = "openai/gpt-oss-20b"

_client = None


def _get_client():
    """Groq client ko lazily banate hain - taaki agar groq package
    ya key missing ho to import-time par hi crash na ho."""

    global _client

    if _client is not None:
        return _client

    if not GROQ_API_KEY:
        return None

    try:
        from groq import Groq
        _client = Groq(api_key=GROQ_API_KEY)
        return _client

    except Exception:
        return None


def _build_prompt(code, language, error_details):

    error_section = "No error occurred. The code ran successfully."

    if error_details:
        err_type = error_details.get("type", "Unknown")
        err_msg = error_details.get("message", "")
        error_section = f"Error Type: {err_type}\nError Message: {err_msg}"

    return f"""You are an expert {language} code reviewer helping a student learn to code.

CODE:
```{language}
{code}
```

{error_section}

Respond with ONLY a valid JSON object (no markdown fences, no extra text) in exactly this shape:

{{
  "suggestions": ["short actionable improvement tip", "..."],
  "explanation": ["plain-English explanation of what a key part of the code does", "..."],
  "error_fix": {{
    "problem": "one-line summary of what went wrong",
    "reason": "why this error happens, in simple terms",
    "fix": "concrete step the student should take to fix it"
  }}
}}

Rules:
- "suggestions": 2-4 concise, specific tips (not generic advice).
- "explanation": 2-5 bullet-style plain-English lines covering the main logic (not a line-by-line dump).
- "error_fix": only include meaningful content if there IS an error. If there is no error, set "error_fix" to null.
- Keep language simple and beginner-friendly, since the user is a student.
- Return JSON only. No commentary before or after."""


def _parse_ai_json(raw_text):

    text = raw_text.strip()

    # Kabhi kabhi model ```json ... ``` fences laga deta hai, unhe hata dete hain
    if text.startswith("```"):
        text = text.strip("`")
        if text.lower().startswith("json"):
            text = text[4:]
        text = text.strip()

    data = json.loads(text)

    suggestions = data.get("suggestions") or []
    explanation = data.get("explanation") or []
    error_fix = data.get("error_fix")

    if not isinstance(suggestions, list):
        suggestions = [str(suggestions)]

    if not isinstance(explanation, list):
        explanation = [str(explanation)]

    return {
        "suggestions": suggestions,
        "explanation": explanation,
        "error_fix": error_fix
    }


def get_ai_review(code, language, error_details=None):

    client = _get_client()

    if client is None:
        return None

    if not code or not code.strip():
        return None

    try:
        prompt = _build_prompt(code, language, error_details)

        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {"role": "system", "content": "You are a precise, JSON-only code review assistant."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.4,
            max_tokens=800,
            timeout=10,
        )

        raw_text = response.choices[0].message.content

        return _parse_ai_json(raw_text)

    except Exception:
        # Chahe network fail ho, rate limit lage, ya JSON parsing toot jaye -
        # hum silently None return karte hain taaki fallback smoothly chal sake.
        return None


# Testing
if __name__ == "__main__":

    sample_code = "for i in range(5):\n    print(i)"

    result = get_ai_review(sample_code, "python", None)

    print(result)