# AI Bug Report Triage Assistant

A beginner-friendly command-line tool that turns messy bug reports into structured JSON using the OpenAI API.

## What It Does

You give the tool a plain-text bug report. It asks an OpenAI model to extract the important triage details, then validates the result against a JSON schema before showing or saving it.

The output includes:

- title
- summary
- severity
- category
- environment
- steps to reproduce
- expected behavior
- actual behavior
- suspected area
- missing information

## Project Files

```text
.
├── bug_triage_assistant/
│   ├── __init__.py
│   ├── cli.py
│   ├── schema.py
│   └── triage.py
├── samples/
│   ├── login_bug.txt
│   └── mobile_checkout_bug.txt
├── .env.example
├── README.md
└── requirements.txt
```

## Setup On Windows PowerShell

Create and activate a virtual environment:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Install dependencies:

```powershell
pip install -r requirements.txt
```

Create your local environment file:

```powershell
Copy-Item .env.example .env
```

Open `.env` and replace `your_openai_api_key_here` with your real OpenAI API key.

Do not commit `.env` or any real API keys to Git.

## Run The Tool

Run it with a sample report:

```powershell
python -m bug_triage_assistant --file samples\login_bug.txt
```

Save JSON to a file:

```powershell
python -m bug_triage_assistant --file samples\mobile_checkout_bug.txt --output triage-output.json
```

Or pass a short report directly:

```powershell
python -m bug_triage_assistant --text "The dashboard is blank after login on Chrome. Expected charts to load."
```

## Example Output

```json
{
  "title": "Login page hangs on spinner after sign in",
  "summary": "After the update, signing in sometimes leaves the user stuck on a loading spinner instead of opening the dashboard.",
  "severity": "high",
  "category": "ui",
  "environment": {
    "os": "Windows 11",
    "browser": "Chrome",
    "app_version": "2.8.1",
    "device": "Windows laptop"
  },
  "steps_to_reproduce": [
    "Open the app in Chrome on Windows 11.",
    "Enter valid login credentials.",
    "Click Sign In."
  ],
  "expected_behavior": "The user should be taken to the account dashboard.",
  "actual_behavior": "The page shows a spinner forever and no error message.",
  "suspected_area": "Authentication or post-login dashboard redirect",
  "missing_information": [
    "Whether this affects all users or only some accounts",
    "Network or console errors from the browser developer tools"
  ]
}
```

## Notes

- The default model is set in `.env.example` as `OPENAI_MODEL=gpt-4.1-mini`.
- You can change the model in your `.env` file without changing the code.
- If the model returns malformed or incomplete JSON, the app raises a validation error instead of silently accepting bad output.

