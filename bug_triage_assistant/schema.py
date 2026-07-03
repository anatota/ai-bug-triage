from jsonschema import Draft202012Validator


BUG_REPORT_SCHEMA = {
    "type": "object",
    "additionalProperties": False,
    "required": [
        "title",
        "summary",
        "severity",
        "category",
        "environment",
        "steps_to_reproduce",
        "expected_behavior",
        "actual_behavior",
        "suspected_area",
        "missing_information",
    ],
    "properties": {
        "title": {
            "type": "string",
            "description": "A short, clear bug title.",
        },
        "summary": {
            "type": "string",
            "description": "One or two sentences describing the issue.",
        },
        "severity": {
            "type": "string",
            "enum": ["low", "medium", "high", "critical"],
        },
        "category": {
            "type": "string",
            "enum": ["ui", "backend", "performance", "security", "data", "integration", "unknown"],
        },
        "environment": {
            "type": "object",
            "additionalProperties": False,
            "required": ["os", "browser", "app_version", "device"],
            "properties": {
                "os": {"type": "string"},
                "browser": {"type": "string"},
                "app_version": {"type": "string"},
                "device": {"type": "string"},
            },
        },
        "steps_to_reproduce": {
            "type": "array",
            "items": {"type": "string"},
        },
        "expected_behavior": {"type": "string"},
        "actual_behavior": {"type": "string"},
        "suspected_area": {"type": "string"},
        "missing_information": {
            "type": "array",
            "items": {"type": "string"},
        },
    },
}


def validate_bug_report(data):
    """Return a list of validation error strings. Empty list means valid."""
    validator = Draft202012Validator(BUG_REPORT_SCHEMA)
    errors = sorted(validator.iter_errors(data), key=lambda error: list(error.path))
    return [format_error(error) for error in errors]


def format_error(error):
    path = ".".join(str(part) for part in error.path)
    location = path or "root"
    return f"{location}: {error.message}"
