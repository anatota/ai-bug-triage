from bug_triage_assistant.schema import validate_bug_report


def valid_bug_report():
    return {
        "title": "Login fails after invalid password",
        "summary": "The app crashes after a user enters the wrong password and clicks login.",
        "severity": "high",
        "category": "ui",
        "environment": {
            "os": "Windows 10",
            "browser": "Chrome",
            "app_version": "unknown",
            "device": "laptop",
        },
        "steps_to_reproduce": [
            "Open the login page.",
            "Enter an incorrect password.",
            "Click login.",
        ],
        "expected_behavior": "The app should show an invalid password message.",
        "actual_behavior": "The app crashes.",
        "suspected_area": "Login form error handling",
        "missing_information": ["Exact app version"],
    }


def test_valid_bug_report_passes_validation():
    errors = validate_bug_report(valid_bug_report())

    assert errors == []


def test_missing_required_field_fails_validation():
    report = valid_bug_report()
    del report["severity"]

    errors = validate_bug_report(report)

    assert any("severity" in error for error in errors)


def test_invalid_severity_fails_validation():
    report = valid_bug_report()
    report["severity"] = "urgent"

    errors = validate_bug_report(report)

    assert any("urgent" in error for error in errors)
