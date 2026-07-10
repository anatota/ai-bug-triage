# AI Bug Triage Assistant

[![Tests](https://github.com/anatota/ai-bug-triage/actions/workflows/tests.yml/badge.svg)](https://github.com/anatota/ai-bug-triage/actions/workflows/tests.yml)

AI Bug Triage Assistant is a Python CLI tool that turns messy bug reports into structured triage JSON using the OpenAI API. It is designed for QA and bug triage workflows where inconsistent reports need to be organized into clear fields such as severity, category, reproduction steps, expected behavior, actual behavior, and missing information.

This is a focused v1 project: a practical command-line workflow with schema validation, automated tests, packaging metadata, Makefile commands, and GitHub Actions CI.

## Demo

![AI Bug Triage CLI demo](assets/ai-bug-triage-demo.gif)

## Features

- CLI input from quoted text, `--text`, or a bug report file
- Structured JSON output for bug triage fields
- JSON schema validation before accepting AI output
- Missing information detection for incomplete reports
- Severity and category suggestions
- Optional output file support
- Automated tests with pytest
- GitHub Actions CI for test runs
- Makefile commands for common local workflows

## Tech Stack

- Python 3.12+
- OpenAI API
- jsonschema
- pytest
- pyproject.toml packaging
- Makefile
- GitHub Actions

## Installation

Clone the repository and move into the project folder:

```bash
git clone git@github.com:anatota/ai-bug-triage.git
cd ai-bug-triage
```

Create and activate a virtual environment.

On Linux/macOS:

```bash
python -m venv .venv
source .venv/bin/activate
```

On Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Install the project with development dependencies:

```bash
make install-dev
```

Create a local environment file:

```bash
cp .env.example .env
```

Then edit `.env` and set your OpenAI API key:

```text
OPENAI_API_KEY=your_openai_api_key_here
OPENAI_MODEL=gpt-4.1-mini
```

Do not commit `.env` or real API keys.

## Usage

Run the CLI with a short bug report:

```bash
python main.py "App crashes when I click the login button after entering a valid email."
```

Run the included example command:

```bash
make run-example
```

Run the CLI with a sample file:

```bash
python main.py --file samples/login_bug.txt
```

Save the structured JSON to a file:

```bash
python main.py --file samples/mobile_checkout_bug.txt --output triage-output.json
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

## Common Commands

Use these commands from the project root after activating your virtual environment:

```bash
make install
```

Install the project in editable mode.

```bash
make install-dev
```

Install the project in editable mode with development dependencies.

```bash
make test
```

Run the test suite with pytest.

```bash
make run-example
```

Run the CLI with an example bug report.

```bash
make clean
```

Remove common Python cache, test, and build artifacts.

## Testing

Tests are run with pytest:

```bash
make test
```

The test suite focuses on deterministic local behavior, including CLI input handling and schema validation. Tests do not rely on live OpenAI API calls where local validation is enough. GitHub Actions also runs the test suite automatically on pushes and pull requests.

## CI

This repository uses GitHub Actions for continuous integration. The workflow is defined in `.github/workflows/tests.yml` and runs:

- dependency installation with `make install-dev`
- the test suite with `make test`

## What This Project Demonstrates

This project demonstrates practical skills relevant to junior QA automation, technical QA, and junior Python roles:

- writing a usable Python CLI tool
- validating structured AI output instead of blindly trusting model responses
- testing core behavior without relying on live API calls where applicable
- packaging a Python project with `pyproject.toml`
- using Makefile commands for a reproducible local workflow
- running automated tests in GitHub Actions CI

## Future Improvements

- Dockerfile and docker-compose for easier local setup
- Optional FastAPI endpoint for HTTP-based triage
- GitHub or Jira issue integration
- Batch processing for multiple bug reports
- Richer test fixtures for more report formats

## Notes

- The default model is set in `.env.example` as `OPENAI_MODEL=gpt-4.1-mini`.
- You can change the model in `.env` without changing the code.
- If the model returns malformed or incomplete JSON, the app raises a validation error instead of silently accepting bad output.
