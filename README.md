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

## Engineering Decisions

### CLI-first design

I built this as a command-line tool instead of a web app to keep the first version simple, scriptable, and easy to test. A CLI is enough for the core workflow: pass in a bug report, get structured triage output back. It can also be extended later into batch processing, GitHub issue creation, or CI/CD automation without needing to rewrite the core logic.

### Environment-based configuration

The OpenAI API key is loaded from a local `.env` file instead of being hardcoded. This keeps secrets out of the repository and allows each user to configure the app locally. The repo includes `.env.example` to show the required variables without exposing real credentials.

### Structured JSON output

The app asks the model to return structured JSON instead of free-form text. This makes the output easier to validate, save, compare, or pass into other tools such as GitHub Issues, Jira, dashboards, or reports.

### JSON schema validation

The app does not blindly trust the AI response. The model output is validated against a strict JSON schema before it is accepted. This helps catch missing fields, invalid severity/category values, malformed JSON, or unexpected extra properties.

### Tests avoid real API calls

The tests focus on deterministic local behavior, such as CLI input handling and schema validation. They do not call the OpenAI API because model output can vary, and real API calls would make tests slower, more expensive, and less reliable.

### Separation of concerns

The project separates CLI handling, AI triage logic, and schema validation into different files. This keeps the code easier to understand, test, and extend.

## Project Files

```text
.
|-- bug_triage_assistant/
|   |-- __init__.py
|   |-- __main__.py
|   |-- cli.py
|   |-- schema.py
|   `-- triage.py
|-- main.py
|-- samples/
|   |-- login_bug.txt
|   `-- mobile_checkout_bug.txt
|-- tests/
|   |-- test_cli.py
|   `-- test_schema.py
|-- .env.example
|-- .gitignore
|-- README.md
|-- requirements-dev.txt
`-- requirements.txt
```

## Setup On Windows 10 In VS Code PowerShell

These steps assume you opened this project folder in VS Code and are using the built-in PowerShell terminal.

In VS Code, open the terminal:

```text
Terminal > New Terminal
```

Make sure the terminal is in the project folder. You should see a path ending in `ai-bug-triage`.

Create a virtual environment:

```powershell
python -m venv .venv
```

Activate the virtual environment:

```powershell
.\.venv\Scripts\Activate.ps1
```

After activation, your prompt should start with `(.venv)`.

Install dependencies:

```powershell
pip install -r requirements.txt
```

Create your local environment file:

```powershell
Copy-Item .env.example .env
```

Open `.env` in VS Code and replace `your_openai_api_key_here` with your real OpenAI API key.

Do not commit `.env` or any real API keys to Git. The `.env` file is only for your local machine and is ignored by `.gitignore`.

## Run The Tool

Run the app with a sample bug report:

```powershell
python main.py --file samples\login_bug.txt
```

You should see structured JSON printed in the terminal.

Run the app with a short bug report typed directly into the command:

```powershell
python main.py "App crashes when I click login after typing wrong password"
```

Save JSON to a file:

```powershell
python main.py --file samples\mobile_checkout_bug.txt --output triage-output.json
```

Or pass a short report directly:

```powershell
python main.py "The dashboard is blank after login on Chrome. Expected charts to load."
```

## Running Tests On Windows

The tests only check local Python logic. They do not call the OpenAI API.

In the VS Code PowerShell terminal, activate your virtual environment:

```powershell
.\.venv\Scripts\Activate.ps1
```

Install the normal app dependencies and the test dependency:

```powershell
pip install -r requirements.txt
pip install -r requirements-dev.txt
```

Run the tests:

```powershell
pytest
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

