# Repository guidance

## Project

AI Bug Triage Assistant is a Python 3.12+ CLI that converts unstructured bug reports into schema-validated triage JSON using the OpenAI API.

## Setup and commands

Run commands from the repository root.

- Install development dependencies: `make install-dev`
- Run the test suite: `make test`
- Run the example CLI command: `make run-example`
- Remove generated Python artifacts: `make clean`

Create `.env` from `.env.example` only for local API-backed runs. Never commit `.env`, API keys, or generated triage output.

## Architecture

- `main.py` is the top-level CLI entry point.
- `bug_triage_assistant/cli.py` parses input, handles user-facing errors, and writes or prints JSON.
- `bug_triage_assistant/triage.py` calls the OpenAI API, parses the response, and invokes validation.
- `bug_triage_assistant/schema.py` owns the JSON Schema and formats validation errors.
- `tests/test_cli.py` covers deterministic CLI input behavior.
- `tests/test_schema.py` covers local schema validation.

Keep CLI concerns, API orchestration, and schema validation in their existing modules unless a change requires a deliberate architectural revision.

## Testing constraints

- Always run `make test` after code changes.
- Tests should be deterministic and must not require a real API key, network access, or paid OpenAI calls.
- Mock external API behavior when testing integration logic.
- If CLI behavior changes, also run the relevant CLI command manually and inspect its exit status and output.
- Use a live OpenAI request only when the task explicitly requires an integration smoke test.

## Definition of done

A change is complete when:

1. The relevant behavior is covered by a test or an existing test proves it.
2. `make test` passes.
3. CLI-facing changes have been exercised through the relevant terminal command.
4. No secrets or unrelated generated files are included in the diff.
5. Documentation is updated when installation, usage, configuration, or observable behavior changes.
