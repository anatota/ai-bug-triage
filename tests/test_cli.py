from argparse import Namespace
from pathlib import Path

import pytest

from bug_triage_assistant import cli


def test_read_report_text_from_argument():
    args = Namespace(file=None, text=None, report="App crashes on login")

    assert cli.read_report_text(args) == "App crashes on login"


def test_read_report_text_from_text_flag():
    args = Namespace(file=None, text="Dashboard is blank", report=None)

    assert cli.read_report_text(args) == "Dashboard is blank"


def test_read_report_text_from_file():
    bug_file = Path("samples/login_bug.txt")
    args = Namespace(file=str(bug_file), text=None, report=None)

    assert "Login is weird after the update" in cli.read_report_text(args)


def test_no_bug_report_shows_helpful_error(monkeypatch, capsys):
    monkeypatch.setattr("sys.argv", ["main.py"])

    with pytest.raises(SystemExit) as error:
        cli.main()

    captured = capsys.readouterr()
    assert error.value.code == 2
    assert "No bug report provided" in captured.err
    assert "python main.py" in captured.err
