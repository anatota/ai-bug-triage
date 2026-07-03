import json
import os

from dotenv import load_dotenv
from openai import OpenAI

from bug_triage_assistant.schema import BUG_REPORT_SCHEMA, validate_bug_report


SYSTEM_PROMPT = """You turn messy user bug reports into structured JSON for software teams.

Rules:
- Return only JSON that matches the provided schema.
- Use "unknown" for environment fields that are not mentioned.
- Keep wording concise and factual.
- Do not invent reproduction steps. If details are missing, list them in missing_information.
- Choose severity based on user impact, data loss, security impact, and whether there is a workaround.
"""


def triage_bug_report(report_text):
    load_dotenv()

    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError(
            "OPENAI_API_KEY is missing. Copy .env.example to .env and add your API key."
        )

    client = OpenAI(api_key=api_key)
    model = os.getenv("OPENAI_MODEL", "gpt-4.1-mini")

    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {
                "role": "user",
                "content": f"Convert this bug report into triage JSON:\n\n{report_text}",
            },
        ],
        response_format={
            "type": "json_schema",
            "json_schema": {
                "name": "bug_report_triage",
                "schema": BUG_REPORT_SCHEMA,
                "strict": True,
            },
        },
    )

    content = response.choices[0].message.content
    try:
        data = json.loads(content)
    except json.JSONDecodeError as error:
        raise ValueError(
            "The model returned invalid JSON. Please try again or simplify the bug report."
        ) from error

    errors = validate_bug_report(data)

    if errors:
        formatted_errors = "\n".join(f"- {error}" for error in errors)
        raise ValueError(f"The model returned JSON, but it did not pass validation:\n{formatted_errors}")

    return data
